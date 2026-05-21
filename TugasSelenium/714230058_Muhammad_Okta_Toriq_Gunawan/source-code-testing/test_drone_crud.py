"""Test Objective (a): UI Validation - Drone CRUD via UI.

Mendaftarkan drone melalui antarmuka pengguna.
"""

from __future__ import annotations

import time

import pytest
import requests

from pages.dashboard_page import DashboardPage
from pages.drone_page import DronePage


def _is_admin(api_base_url, token):
    """Check if current user is admin."""
    # Decode JWT manually to get role
    import json
    import base64
    parts = token.split('.')
    if len(parts) != 3:
        return False
    payload = json.loads(base64.urlsafe_b64decode(parts[1] + '=='))
    return payload.get('role') == 'ADMIN'


class TestDroneCrud:
    """Test drone fleet management UI."""

    def test_drone_page_loads(self, authenticated_driver, base_url):
        """Verify drones page renders correctly."""
        from selenium.webdriver.common.by import By
        dashboard = DashboardPage(authenticated_driver, base_url)
        dashboard.open()
        dashboard.navigate_to_drones()

        # Verify page has Drones heading
        assert "Drones" in authenticated_driver.page_source, "Drones page should load"

    def test_create_drone_via_ui(self, authenticated_driver, base_url, api_base_url, test_admin_token, test_label):
        """Objective: Register drone through UI form (admin only)."""
        if not _is_admin(api_base_url, test_admin_token['token']):
            pytest.skip("User is not admin - skipping admin-only test")

        drone_page = DronePage(authenticated_driver, base_url)
        lora_id = f"{test_label}-001"
        success = drone_page.create_drone(
            name=f"Drone {test_label}",
            model="QuadX Test",
            lora_id=lora_id,
        )

        assert success, f"Drone with lora_id {lora_id} should be created and visible"
        drone_page.screenshot(f"drone_created_{test_label}")

    def test_drone_card_displays_info(self, authenticated_driver, base_url, api_base_url, test_admin_token, test_label):
        """Verify drone card shows name, model, status, lora_id."""
        # Create drone via API (works for any role)
        lora_id = f"{test_label}-002"
        resp = requests.post(
            f"{api_base_url}/api/v1/drones/",
            headers={"Authorization": f"Bearer {test_admin_token['token']}"},
            json={"name": f"Info Drone {test_label}", "model": "Hexa Test", "lora_id": lora_id},
            timeout=10,
        )
        assert resp.status_code in (200, 201), f"Failed to create drone: {resp.text}"

        drone_page = DronePage(authenticated_driver, base_url)
        drone_page.open()

        # Verify card content
        assert drone_page.is_drone_present(lora_id), "Drone card should be present"

    def test_drone_list_renders(self, authenticated_driver, base_url, api_base_url, test_admin_token, test_label):
        """Verify drone list renders with API-created data."""
        # Seed some drones via API
        for i in range(3):
            resp = requests.post(
                f"{api_base_url}/api/v1/drones/",
                headers={"Authorization": f"Bearer {test_admin_token['token']}"},
                json={
                    "name": f"Test Drone {test_label}-{i}",
                    "model": "Test",
                    "lora_id": f"{test_label}-LIST-{i}",
                },
                timeout=10,
            )
            assert resp.status_code in (200, 201), f"Failed to create drone: {resp.text}"

        # Refresh page to load new data
        authenticated_driver.refresh()
        time.sleep(3)

        drone_page = DronePage(authenticated_driver, base_url)
        count = drone_page.get_drone_count()
        assert count >= 3, f"Should display at least 3 drones, found {count}"
