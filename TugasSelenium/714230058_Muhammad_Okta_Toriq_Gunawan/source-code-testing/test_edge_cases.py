"""Test Objective (d): Bug Discovery / Edge Cases.

Menemukan dan mendokumentasikan cacat sistem sedini mungkin.
"""

from __future__ import annotations

import json
import time

import pytest
import requests

from pages.auth_page import AuthPage
from pages.dashboard_page import DashboardPage
from pages.telemetry_page import TelemetryPage
from utils.mock_drone import MockDronePublisher


class TestEdgeCases:
    """Defect discovery tests."""

    def test_invalid_mqtt_payload_not_crash_frontend(
        self,
        authenticated_driver,
        base_url,
        api_base_url,
        test_admin_token,
        test_label,
    ):
        """Bug: Invalid JSON payload should not crash frontend."""
        lora_id = f"{test_label}-INVALID"
        requests.post(
            f"{api_base_url}/api/v1/drones/",
            headers={"Authorization": f"Bearer {test_admin_token['token']}"},
            json={"name": "Invalid Drone", "model": "Test", "lora_id": lora_id},
            timeout=30,
        )

        # Publish invalid JSON directly via MQTT
        import paho.mqtt.client as mqtt
        client = mqtt.Client()
        client.connect("broker.hivemq.com", 1883, 60)
        client.publish("aerialcast/telemetry", "this is not json { broken")
        client.disconnect()

        time.sleep(5)

        # Frontend should still be responsive
        dashboard = DashboardPage(authenticated_driver, base_url)
        dashboard.open()
        assert dashboard.assert_dashboard_loaded(), "Dashboard should not crash after invalid payload"

    def test_missing_lora_id_ignored_gracefully(
        self,
        authenticated_driver,
        base_url,
        api_base_url,
        test_admin_token,
        test_label,
    ):
        """Bug: Payload without lora_id should be ignored gracefully."""
        mock = MockDronePublisher()
        payload = {
            "lat": -6.200,
            "lon": 106.800,
            "vbat": 12.0,
            "time": "2025-05-21T10:00:00Z",
        }
        mock.client.connect(mock.broker, mock.port, 60)
        mock.client.publish(mock.topic, json.dumps(payload))
        mock.client.disconnect()

        time.sleep(5)

        dashboard = DashboardPage(authenticated_driver, base_url)
        dashboard.open()
        assert dashboard.assert_dashboard_loaded(), "Frontend should be stable after missing lora_id payload"

    def test_expired_token_redirect(
        self,
        driver,
        base_url,
    ):
        """Bug: Expired token should redirect to auth, not infinite loop."""
        # Inject fake expired token
        driver.get(base_url)
        time.sleep(1)
        driver.execute_script("localStorage.setItem('token', 'fake_expired_token_xyz');")
        driver.refresh()
        time.sleep(3)

        # Should end up on /auth page
        assert "/auth" in driver.current_url, "Should redirect to auth when token is invalid"

    def test_double_polling_no_memory_leak(
        self,
        authenticated_driver,
        base_url,
        api_base_url,
        test_admin_token,
        test_label,
    ):
        """Bug: Navigating away and back should not create double polling intervals."""
        lora_id = f"{test_label}-POLL"
        requests.post(
            f"{api_base_url}/api/v1/drones/",
            headers={"Authorization": f"Bearer {test_admin_token['token']}"},
            json={"name": "Poll Drone", "model": "Test", "lora_id": lora_id},
            timeout=30,
        )

        mock = MockDronePublisher(lora_id=lora_id)
        mock.start(interval=2.0, count=10)

        dashboard = DashboardPage(authenticated_driver, base_url)
        dashboard.open()
        time.sleep(5)

        # Navigate away and back multiple times
        for _ in range(3):
            dashboard.navigate_to_drones()
            time.sleep(2)
            dashboard.navigate_to_missions()
            time.sleep(2)
            dashboard.open()  # Back to dashboard
            time.sleep(2)

        time.sleep(10)

        # Check no console errors from duplicate intervals
        assert not dashboard.has_console_errors(), "No errors from double polling"

        mock.stop()

    def test_role_access_control(
        self,
        driver,
        base_url,
        api_base_url,
        test_label,
    ):
        """Bug: Non-admin should not access admin-only pages/features."""
        # Register a pilot user (non-admin)
        email = f"{test_label}-pilot@aerialcast.test"
        password = "TestPass123!"
        requests.post(
            f"{api_base_url}/auth/register",
            json={"email": email, "password": password, "full_name": "Test Pilot"},
            timeout=30,
        )

        login_resp = requests.post(
            f"{api_base_url}/auth/login",
            json={"email": email, "password": password},
            timeout=30,
        )
        pilot_token = login_resp.json()["access_token"]

        # Try admin-only endpoint
        resp = requests.post(
            f"{api_base_url}/api/v1/missions/some-id/status/approve",
            headers={"Authorization": f"Bearer {pilot_token}"},
            timeout=30,
        )
        assert resp.status_code in [403, 404, 400], "Pilot should not be able to approve missions"

    def test_drone_duplicate_lora_id(
        self,
        api_base_url,
        test_admin_token,
        test_label,
    ):
        """Bug: Creating drone with duplicate lora_id should fail gracefully."""
        lora_id = f"{test_label}-DUPE"

        # First creation
        r1 = requests.post(
            f"{api_base_url}/api/v1/drones/",
            headers={"Authorization": f"Bearer {test_admin_token['token']}"},
            json={"name": "First", "model": "Test", "lora_id": lora_id},
            timeout=30,
        )
        assert r1.status_code == 200

        # Duplicate
        r2 = requests.post(
            f"{api_base_url}/api/v1/drones/",
            headers={"Authorization": f"Bearer {test_admin_token['token']}"},
            json={"name": "Second", "model": "Test", "lora_id": lora_id},
            timeout=30,
        )
        assert r2.status_code in [409, 400, 422], "Duplicate lora_id should be rejected"

    def test_map_render_after_refresh(
        self,
        authenticated_driver,
        base_url,
        api_base_url,
        test_admin_token,
        test_label,
    ):
        """Bug: Leaflet map should render correctly after page refresh."""
        lora_id = f"{test_label}-MAP"
        requests.post(
            f"{api_base_url}/api/v1/drones/",
            headers={"Authorization": f"Bearer {test_admin_token['token']}"},
            json={"name": "Map Drone", "model": "Test", "lora_id": lora_id},
            timeout=30,
        )

        dashboard = DashboardPage(authenticated_driver, base_url)
        dashboard.open()

        telemetry = TelemetryPage(authenticated_driver, base_url)
        assert telemetry.assert_map_rendered(), "Map should render initially"

        # Refresh page
        authenticated_driver.refresh()
        time.sleep(3)

        assert telemetry.assert_map_rendered(), "Map should render after refresh"

    def test_console_errors_on_dashboard_load(
        self,
        authenticated_driver,
        base_url,
    ):
        """Bug: Dashboard should not produce console errors on load."""
        dashboard = DashboardPage(authenticated_driver, base_url)
        dashboard.open()
        time.sleep(3)

        errors = dashboard.has_console_errors()
        assert not errors, "Dashboard should not have SEVERE console errors"
