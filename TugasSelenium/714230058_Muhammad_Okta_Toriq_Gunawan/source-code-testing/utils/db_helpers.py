"""Database helpers for test verification and cleanup."""

from __future__ import annotations

import os
import warnings

import psycopg2
from psycopg2.extras import RealDictCursor

warnings.filterwarnings("ignore", category=UserWarning)


class DBHelper:
    """Helper to interact with the Neon staging database."""

    def __init__(self):
        self.database_url = os.getenv(
            "DATABASE_URL",
            " ",
        )
        self.conn = None

    def _get_connection(self):
        if self.conn is None or self.conn.closed:
            self.conn = psycopg2.connect(self.database_url, cursor_factory=RealDictCursor)
        return self.conn

    def cleanup_test_data(self):
        """Delete all rows created by tests (identified by TEST- prefix)."""
        conn = self._get_connection()
        cur = conn.cursor()

        # Order matters due to FK constraints
        cleanup_statements = [
            "DELETE FROM telemetry_data WHERE session_id IN (SELECT session_id FROM flight_sessions WHERE mission_id IN (SELECT mission_id FROM missions WHERE mission_name LIKE 'TEST-%'));",
            "DELETE FROM alerts WHERE session_id IN (SELECT session_id FROM flight_sessions WHERE mission_id IN (SELECT mission_id FROM missions WHERE mission_name LIKE 'TEST-%'));",
            "DELETE FROM flight_sessions WHERE mission_id IN (SELECT mission_id FROM missions WHERE mission_name LIKE 'TEST-%');",
            "DELETE FROM mission_waypoints WHERE mission_id IN (SELECT mission_id FROM missions WHERE mission_name LIKE 'TEST-%');",
            "DELETE FROM mission_preflight_checklists WHERE mission_id IN (SELECT mission_id FROM missions WHERE mission_name LIKE 'TEST-%');",
            "DELETE FROM mission_postflight_checklists WHERE mission_id IN (SELECT mission_id FROM missions WHERE mission_name LIKE 'TEST-%');",
            "DELETE FROM missions WHERE mission_name LIKE 'TEST-%';",
            "DELETE FROM drones WHERE lora_id LIKE 'TEST-%';",
            # Preserve session-scoped test user - don't delete users
            # "DELETE FROM users WHERE email LIKE '%@aerialcast.test';",
        ]

        for stmt in cleanup_statements:
            try:
                cur.execute(stmt)
            except Exception as e:
                print(f"[DB Cleanup Skip] {e}")

        conn.commit()
        cur.close()

    def get_telemetry_for_session(self, session_id: str, limit: int = 10):
        """Fetch telemetry rows for a session."""
        conn = self._get_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM telemetry_data WHERE session_id = %s ORDER BY time DESC LIMIT %s;",
            (session_id, limit),
        )
        rows = cur.fetchall()
        cur.close()
        return rows

    def get_drone_by_lora_id(self, lora_id: str):
        """Fetch drone by lora_id."""
        conn = self._get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM drones WHERE lora_id = %s LIMIT 1;", (lora_id,))
        row = cur.fetchone()
        cur.close()
        return row

    def get_mission_by_name(self, mission_name: str):
        """Fetch mission by name."""
        conn = self._get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM missions WHERE mission_name = %s LIMIT 1;", (mission_name,))
        row = cur.fetchone()
        cur.close()
        return row

    def get_latest_session_for_mission(self, mission_id: str):
        """Fetch latest flight session for a mission."""
        conn = self._get_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM flight_sessions WHERE mission_id = %s ORDER BY start_time DESC LIMIT 1;",
            (mission_id,),
        )
        row = cur.fetchone()
        cur.close()
        return row

    def count_telemetry_rows(self, session_id: str) -> int:
        """Count telemetry rows for a session."""
        conn = self._get_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT COUNT(*) as cnt FROM telemetry_data WHERE session_id = %s;",
            (session_id,),
        )
        row = cur.fetchone()
        cur.close()
        return row["cnt"] if row else 0

    def close(self):
        if self.conn and not self.conn.closed:
            self.conn.close()
