"""In-memory ring buffer of generated alerts for dashboards and SOAR."""

from __future__ import annotations

import threading
from collections import deque
from typing import Any

_lock = threading.Lock()
_alerts: deque = deque(maxlen=500)


def record_alert(alert: dict[str, Any]) -> None:
    if not alert:
        return
    with _lock:
        _alerts.append(alert)


def get_alerts() -> list[dict[str, Any]]:
    with _lock:
        return list(_alerts)
