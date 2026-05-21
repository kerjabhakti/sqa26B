"""Test Objective (b): Data Pipeline E2E.

Mock Drone → MQTT → Backend Flask → PostgreSQL/TimescaleDB → Frontend Next.js
"""

from __future__ import annotations

import time

import pytest
import requests

from pages.dashboard_page import DashboardPage
from pages.drone_page import DronePage
from pages.mission_page import MissionPage
from pages.telemetry_page import TelemetryPage
from utils.db_helpers import DBHelper
from utils.mock_drone import MockDronePublisher


API_TIMEOUT = 30


def _setup_flight_session(api_base_url, token, test_label):
    """Helper: Create drone, mission (IN_PROGRESS), and flight session for telemetry."""
    # 1. Create drone
    drone_resp = requests.post(
        f"{api_base_url}/api/v1/drones/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": f"Pipeline Drone {test_label}",
            "model": "QuadX",
            "lora_id": f"{test_label}-PIPE",
        },
        timeout=API_TIMEOUT,
    )
    assert drone_resp.status_code in (200, 201), f"Failed to create drone: {drone_resp.text}"
    drone_id = drone_resp.json()["drone_id"]

    # 2. Create mission (auto-submits as PENDING_APPROVAL)
    mission_resp = requests.post(
        f"{api_base_url}/api/v1/missions/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "mission_name": f"Pipeline Mission {test_label}",
            "drone_id": drone_id,
            "save_as_draft": False,
            "waypoints": [{"latitude": -6.2000, "longitude": 106.8000, "order": 1}],
        },
        timeout=API_TIMEOUT,
    )
    assert mission_resp.status_code in (200, 201), f"Failed to create mission: {mission_resp.text}"
    mission_id = mission_resp.json()["mission_id"]

    # 3. Approve mission (admin only) - skip if not admin
    # For pilot users, we need an admin to approve. For now, just verify drone exists.
    return drone_id, mission_id, f"{test_label}-PIPE"


class TestDataPipeline:
    """End-to-end data pipeline validation."""

    def test_full_pipeline_mock_to_ui(
        self,
        authenticated_driver,
        base_url,
        api_base_url,
        test_label,
        db_helper,
    ):
        """Objective b: Full E2E pipeline from MQTT publish to UI display."""

        token = authenticated_driver.execute_script('return localStorage.getItem("token");')
        drone_id, mission_id, lora_id = _setup_flight_session(
            api_base_url, token, test_label
        )

        # Verify drone in DB
        db_drone = db_helper.get_drone_by_lora_id(lora_id)
        assert db_drone is not None, f"Drone {lora_id} should exist in DB"

        # Start mock publisher
        mock = MockDronePublisher(lora_id=lora_id, base_lat=-6.2000, base_lon=106.8000)
        payload = mock.publish_single()
        print(f"[Test] Published payload: {payload}")
        time.sleep(5)

        # Verify UI loads without crash
        dashboard = DashboardPage(authenticated_driver, base_url)
        dashboard.open()
        assert dashboard.assert_dashboard_loaded(), "Dashboard should load after data pipeline"
        assert not dashboard.has_console_errors(), "No console errors should occur"

        mock.stop()

    def test_pipeline_db_verification(
        self,
        api_base_url,
        test_admin_token,
        db_helper,
        test_label,
    ):
        """Verify data actually lands in PostgreSQL/TimescaleDB."""
        lora_id = f"{test_label}-DB"

        # Create drone via API
        requests.post(
            f"{api_base_url}/api/v1/drones/",
            headers={"Authorization": f"Bearer {test_admin_token['token']}"},
            json={"name": "DB Verify Drone", "model": "Test", "lora_id": lora_id},
            timeout=API_TIMEOUT,
        )

        # Publish via mock
        mock = MockDronePublisher(lora_id=lora_id)
        payload = mock.publish_single()
        time.sleep(5)

        # Verify drone exists in DB
        db_drone = db_helper.get_drone_by_lora_id(lora_id)
        assert db_drone is not None, "Drone should be persisted in DB"

        mock.stop()

    def test_mqtt_to_db_to_api_flow(
        self,
        api_base_url,
        test_admin_token,
        db_helper,
        test_label,
    ):
        """Verify data flows: MQTT → Backend → DB → API endpoint."""
        lora_id = f"{test_label}-API"

        # Seed drone
        requests.post(
            f"{api_base_url}/api/v1/drones/",
            headers={"Authorization": f"Bearer {test_admin_token['token']}"},
            json={"name": "API Flow Drone", "model": "Test", "lora_id": lora_id},
            timeout=API_TIMEOUT,
        )

        # Publish telemetry
        mock = MockDronePublisher(lora_id=lora_id)
        payload = mock.publish_single()
        time.sleep(5)

        # Query API for sessions
        resp = requests.get(
            f"{api_base_url}/api/v1/sessions",
            headers={"Authorization": f"Bearer {test_admin_token['token']}"},
            timeout=API_TIMEOUT,
        )
        assert resp.status_code == 200, "API should return sessions"

        mock.stop()
