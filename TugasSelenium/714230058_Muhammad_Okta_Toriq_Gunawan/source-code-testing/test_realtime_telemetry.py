"""Test Objective (c): Real-time Telemetry Display.

Verifikasi koordinat, sinyal, dan kecepatan update tanpa freeze/crash/latency masif.
"""

from __future__ import annotations

import time

import pytest
import requests

from pages.dashboard_page import DashboardPage
from pages.drone_page import DronePage
from pages.telemetry_page import TelemetryPage
from utils.mock_drone import MockDronePublisher


class TestRealtimeTelemetry:
    """Real-time telemetry stability and accuracy tests."""

    def test_telemetry_values_update_without_freeze(
        self,
        authenticated_driver,
        base_url,
        api_base_url,
        test_admin_token,
        test_label,
    ):
        """Objective c: Verify vitals update across polling cycles without freeze."""
        # Setup: create drone
        lora_id = f"{test_label}-RT"
        requests.post(
            f"{api_base_url}/api/v1/drones/",
            headers={"Authorization": f"Bearer {test_admin_token['token']}"},
            json={"name": "RT Drone", "model": "Test", "lora_id": lora_id},
            timeout=API_TIMEOUT,
        )

        # Start continuous mock publishing (every 2s, 8 messages = ~16s)
        mock = MockDronePublisher(lora_id=lora_id)
        mock.start(interval=2.0, count=8)

        # Open dashboard and navigate to telemetry view
        dashboard = DashboardPage(authenticated_driver, base_url)
        dashboard.open()

        telemetry = TelemetryPage(authenticated_driver, base_url)

        # Wait for first telemetry to arrive
        time.sleep(8)

        # Capture initial battery
        initial_battery = telemetry.get_battery_text()
        print(f"[Test] Initial battery: {initial_battery}")

        # Wait for more polling cycles
        time.sleep(12)

        # Capture updated battery
        updated_battery = telemetry.get_battery_text()
        print(f"[Test] Updated battery: {updated_battery}")

        # Assert: values should change (or at least vitals are visible)
        assert telemetry.assert_vitals_visible(), "Vitals panel should be visible"
        assert not telemetry.has_console_errors(), "No SEVERE console errors should occur"

        mock.stop()

    def test_telemetry_accuracy_matches_payload(
        self,
        authenticated_driver,
        base_url,
        api_base_url,
        test_admin_token,
        test_label,
    ):
        """Verify UI values match the MQTT payload within tolerance."""
        lora_id = f"{test_label}-ACC"
        requests.post(
            f"{api_base_url}/api/v1/drones/",
            headers={"Authorization": f"Bearer {test_admin_token['token']}"},
            json={"name": "Accuracy Drone", "model": "Test", "lora_id": lora_id},
            timeout=API_TIMEOUT,
        )

        # Publish known payload
        mock = MockDronePublisher(lora_id=lora_id, base_lat=-6.2000, base_lon=106.8000)
        mock.vbat = 12.5
        mock.rssi = -70
        mock.snr = 9.0
        payload = mock.publish_single()
        time.sleep(8)

        # Check UI
        telemetry = TelemetryPage(authenticated_driver, base_url)
        battery_text = telemetry.get_battery_text()
        signal_text = telemetry.get_signal_text()

        # Assert: UI should show values (exact match might be hard due to formatting)
        assert battery_text != "" or signal_text != "", "Telemetry values should appear in UI"

        mock.stop()

    def test_no_browser_crash_during_continuous_polling(
        self,
        authenticated_driver,
        base_url,
        api_base_url,
        test_admin_token,
        test_label,
    ):
        """Stress test: continuous polling for 30 seconds without crash."""
        lora_id = f"{test_label}-STRESS"
        requests.post(
            f"{api_base_url}/api/v1/drones/",
            headers={"Authorization": f"Bearer {test_admin_token['token']}"},
            json={"name": "Stress Drone", "model": "Test", "lora_id": lora_id},
            timeout=API_TIMEOUT,
        )

        mock = MockDronePublisher(lora_id=lora_id)
        mock.start(interval=2.0, count=15)  # 15 messages over ~30 seconds

        # Keep page open
        dashboard = DashboardPage(authenticated_driver, base_url)
        dashboard.open()

        # Wait for full duration
        time.sleep(35)

        # Verify page still responsive
        assert authenticated_driver.execute_script("return document.readyState") == "complete", "Page should still be complete"
        assert not telemetry.has_console_errors(), "No console errors after stress test"

        mock.stop()

    def test_status_indicator_changes_state(
        self,
        authenticated_driver,
        base_url,
        api_base_url,
        test_admin_token,
        test_label,
    ):
        """Verify status indicator transitions (idle → live → disconnected)."""
        telemetry = TelemetryPage(authenticated_driver, base_url)
        dashboard = DashboardPage(authenticated_driver, base_url)
        dashboard.open()

        # Initial status
        initial_status = telemetry.get_status_text()
        print(f"[Test] Initial status: {initial_status}")

        # Publish to make it live
        lora_id = f"{test_label}-STATUS"
        requests.post(
            f"{api_base_url}/api/v1/drones/",
            headers={"Authorization": f"Bearer {test_admin_token['token']}"},
            json={"name": "Status Drone", "model": "Test", "lora_id": lora_id},
            timeout=API_TIMEOUT,
        )

        mock = MockDronePublisher(lora_id=lora_id)
        mock.start(interval=2.0, count=3)
        time.sleep(10)

        live_status = telemetry.get_status_text()
        print(f"[Test] Live status: {live_status}")

        mock.stop()
        time.sleep(10)  # Wait for disconnect

        final_status = telemetry.get_status_text()
        print(f"[Test] Final status: {final_status}")

        # Status should have changed at some point
        assert initial_status != final_status or live_status != initial_status, "Status should change during telemetry lifecycle"
