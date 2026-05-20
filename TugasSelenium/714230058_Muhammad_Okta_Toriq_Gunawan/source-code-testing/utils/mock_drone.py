"""Mock drone MQTT publisher for telemetry testing."""

from __future__ import annotations

import json
import os
import random
import threading
import time

import paho.mqtt.client as mqtt


class MockDronePublisher:
    """Simulates a drone publishing telemetry to MQTT broker."""

    DEFAULT_BROKER = os.getenv("MQTT_BROKER", "broker.hivemq.com")
    DEFAULT_PORT = int(os.getenv("MQTT_PORT", "1883"))
    DEFAULT_TOPIC = os.getenv("MQTT_TOPIC", "aerialcast/telemetry")

    def __init__(
        self,
        lora_id: str = "TEST-DRONE-001",
        base_lat: float = -6.2000,
        base_lon: float = 106.8000,
        broker: str | None = None,
        port: int | None = None,
        topic: str | None = None,
    ):
        self.lora_id = lora_id
        self.lat = base_lat
        self.lon = base_lon
        self.alt = 50.0
        self.vbat = 12.4
        self.rssi = -75
        self.snr = 8.5

        self.broker = broker or self.DEFAULT_BROKER
        self.port = port or self.DEFAULT_PORT
        self.topic = topic or self.DEFAULT_TOPIC

        self.client = mqtt.Client()
        self._running = False
        self._thread: threading.Thread | None = None
        self._publish_count = 0

    def _drift(self):
        """Slightly drift coordinates to simulate movement."""
        # Drift ~0.0001 degrees (~11 meters)
        self.lat += random.uniform(-0.0002, 0.0002)
        self.lon += random.uniform(-0.0002, 0.0002)
        self.alt += random.uniform(-2.0, 2.0)
        self.alt = max(0, min(200, self.alt))

        # Slowly drain battery
        self.vbat -= random.uniform(0.01, 0.05)
        self.vbat = max(10.0, self.vbat)

        # Fluctuate signal
        self.rssi = int(random.uniform(-85, -65))
        self.snr = round(random.uniform(5.0, 12.0), 1)

    def _build_payload(self) -> dict:
        """Build the telemetry JSON payload."""
        self._drift()
        self._publish_count += 1
        payload = {
            "lora_id": self.lora_id,
            "lat": round(self.lat, 6),
            "lon": round(self.lon, 6),
            "alt": round(self.alt, 2),
            "vbat": round(self.vbat, 2),
            "rssi": self.rssi,
            "snr": self.snr,
            "time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "test_sequence": self._publish_count,
        }
        return payload

    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print(f"[MockDrone] Connected to MQTT broker: {self.broker}")
        else:
            print(f"[MockDrone] Connection failed with code {rc}")

    def _publish_loop(self, interval: float = 2.0, count: int | None = None):
        """Internal loop that publishes telemetry."""
        self.client.on_connect = self._on_connect
        self.client.connect(self.broker, self.port, 60)
        self.client.loop_start()

        time.sleep(1)

        published = 0
        while self._running:
            payload = self._build_payload()
            self.client.publish(self.topic, json.dumps(payload))
            print(
                f"[MockDrone] Published #{self._publish_count}: "
                f"lat={payload['lat']}, lon={payload['lon']}, vbat={payload['vbat']}"
            )
            published += 1

            if count is not None and published >= count:
                break

            time.sleep(interval)

        self.client.loop_stop()
        self.client.disconnect()
        print("[MockDrone] Publisher stopped.")

    def start(self, interval: float = 2.0, count: int | None = None):
        """Start publishing telemetry in a background thread."""
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(
            target=self._publish_loop,
            args=(interval, count),
            daemon=True,
        )
        self._thread.start()

    def stop(self):
        """Stop the publisher."""
        self._running = False
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=5)
        self.client.loop_stop()
        self.client.disconnect()

    def publish_single(self) -> dict:
        """Publish exactly one message and return the payload."""
        self.client.on_connect = self._on_connect
        self.client.connect(self.broker, self.port, 60)
        self.client.loop_start()
        time.sleep(1)

        payload = self._build_payload()
        self.client.publish(self.topic, json.dumps(payload))
        print(
            f"[MockDrone] Single publish #{self._publish_count}: "
            f"lat={payload['lat']}, lon={payload['lon']}"
        )

        self.client.loop_stop()
        self.client.disconnect()
        return payload
