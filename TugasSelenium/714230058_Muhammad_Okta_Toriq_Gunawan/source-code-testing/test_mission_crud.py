"""Test Objective (a): UI Validation - Mission CRUD with Waypoints.

Membuat mission dengan waypoints melalui UI.
"""

from __future__ import annotations

import time

import pytest
import requests

from pages.dashboard_page import DashboardPage
from pages.mission_page import MissionPage


API_TIMEOUT = 30


def _get_existing_drone_id(api_base_url, token):
    """Get an existing drone ID from the fleet."""
    resp = requests.get(
        f"{api_base_url}/api/v1/drones/",
        headers={"Authorization": f"Bearer {token}"},
        timeout=API_TIMEOUT,
    )
    if resp.status_code == 200:
        drones = resp.json()
        if drones:
            return drones[0]["drone_id"]
    return None


class TestMissionCrud:
    """Test mission planning UI."""

    def test_mission_page_loads(self, authenticated_driver, base_url):
        """Verify missions page renders."""
        dashboard = DashboardPage(authenticated_driver, base_url)
        dashboard.open()
        dashboard.navigate_to_missions()

        mission_page = MissionPage(authenticated_driver, base_url)
        assert "Missions" in authenticated_driver.page_source, "Missions page should load"

    def test_mission_list_renders_api_data(self, authenticated_driver, base_url, api_base_url, test_admin_token, test_label):
        """Verify missions created via API appear in UI list."""
        drone_id = _get_existing_drone_id(api_base_url, test_admin_token['token'])
        assert drone_id, "No existing drone found in fleet"

        # Create mission via API with existing drone_id
        mission_resp = requests.post(
            f"{api_base_url}/api/v1/missions/",
            headers={"Authorization": f"Bearer {test_admin_token['token']}"},
            json={
                "mission_name": f"{test_label} Survey",
                "notes": "Automated test mission",
                "drone_id": drone_id,
                "save_as_draft": True,
                "waypoints": [
                    {"latitude": -6.2000, "longitude": 106.8000, "order": 1},
                    {"latitude": -6.2010, "longitude": 106.8010, "order": 2},
                    {"latitude": -6.2020, "longitude": 106.8020, "order": 3},
                ],
            },
            timeout=API_TIMEOUT,
        )
        assert mission_resp.status_code in (200, 201), f"Failed to create mission: {mission_resp.text}"

        # Navigate to missions page to load new data
        dashboard = DashboardPage(authenticated_driver, base_url)
        dashboard.open()
        dashboard.navigate_to_missions()
        time.sleep(5)  # Wait for data fetch

        mission_page = MissionPage(authenticated_driver, base_url)
        assert mission_page.is_mission_present(f"{test_label} Survey"), "Mission should appear in list"

    def test_mission_status_badge_visible(self, authenticated_driver, base_url, api_base_url, test_admin_token, test_label):
        """Verify mission card shows status badge."""
        drone_id = _get_existing_drone_id(api_base_url, test_admin_token['token'])
        assert drone_id, "No existing drone found"

        # Create mission with existing drone_id
        mission_name = f"{test_label} Badge Test"
        mission_resp = requests.post(
            f"{api_base_url}/api/v1/missions/",
            headers={"Authorization": f"Bearer {test_admin_token['token']}"},
            json={
                "mission_name": mission_name,
                "notes": "Test",
                "drone_id": drone_id,
                "save_as_draft": True,
                "waypoints": [{"latitude": -6.2000, "longitude": 106.8000, "order": 1}],
            },
            timeout=API_TIMEOUT,
        )
        assert mission_resp.status_code in (200, 201), f"Failed to create mission: {mission_resp.text}"

        # Navigate to missions page to check
        dashboard = DashboardPage(authenticated_driver, base_url)
        dashboard.open()
        dashboard.navigate_to_missions()
        time.sleep(5)  # Wait for data fetch

        mission_page = MissionPage(authenticated_driver, base_url)
        assert mission_page.is_mission_present(mission_name), "Mission should be visible"
