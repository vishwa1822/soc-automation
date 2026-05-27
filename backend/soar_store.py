"""Thread-safe SOAR orchestration state (playbooks, IP block list, automation flags)."""

from __future__ import annotations

import copy
import threading
from typing import Any

from alert_store import get_alerts

_lock = threading.Lock()

_DEFAULT_PLAYBOOKS: list[dict[str, Any]] = [
    {"id": "pb-contain-login", "name": "Contain Suspicious Login", "trigger": "Impossible travel + MFA failures", "owner": "IAM", "enabled": True},
    {"id": "pb-isolate-host", "name": "Isolate Compromised Host", "trigger": "Critical malware beacon", "owner": "Endpoint", "enabled": True},
    {"id": "pb-honeytoken", "name": "Honeytoken Response", "trigger": "Credential/file token touched", "owner": "SOC", "enabled": True},
    {"id": "pb-ip-block", "name": "Block Malicious IP", "trigger": "Repeated high-severity scanning", "owner": "Network", "enabled": True},
]

_state: dict[str, Any] = {
    "automation_on": True,
    "auto_block_enabled": True,
    "risk_threshold": 70,
    "blocked_ips": [],
    "playbooks": copy.deepcopy(_DEFAULT_PLAYBOOKS),
    "last_message": "",
}


def _risk_from_severity(severity: str) -> int:
    s = (severity or "LOW").upper()
    if s == "CRITICAL":
        return 92
    if s == "HIGH":
        return 78
    if s == "MEDIUM":
        return 62
    return 44


def _alert_risk_score(alert: dict[str, Any]) -> int:
    """Prefer engine risk_score; fall back to severity bands (matches UI logic)."""
    rs = alert.get("risk_score")
    if isinstance(rs, (int, float)) and 0 <= float(rs) <= 100:
        return int(float(rs))
    return _risk_from_severity(str(alert.get("severity") or "LOW"))


def get_state() -> dict[str, Any]:
    with _lock:
        playbooks = copy.deepcopy(_state["playbooks"])
        blocked = list(_state["blocked_ips"])
        automation_on = bool(_state["automation_on"])
        auto_block = bool(_state["auto_block_enabled"])
        threshold = int(_state["risk_threshold"])
        last_message = str(_state.get("last_message") or "")

    triggers_count = 0
    try:
        from honeytokens.engine_instance import honeytoken_engine

        triggers_count = len(honeytoken_engine.get_trigger_history() or [])
    except Exception:
        pass

    auto_actions = len(blocked) + triggers_count
    alerts = get_alerts()
    avg_risk = 0
    if alerts:
        total = sum(_alert_risk_score(a) for a in alerts)
        avg_risk = round(total / len(alerts))

    active_playbooks = sum(1 for p in playbooks if p.get("enabled"))

    return {
        "automation_on": automation_on,
        "auto_block_enabled": auto_block,
        "risk_threshold": threshold,
        "blocked_ips": blocked,
        "playbooks": playbooks,
        "last_message": last_message,
        "automation_actions_count": auto_actions,
        "active_playbooks": active_playbooks,
        "playbooks_total": len(playbooks),
        "avg_risk_score": avg_risk,
    }


def set_message(msg: str) -> None:
    with _lock:
        _state["last_message"] = msg


def set_automation(enabled: bool) -> None:
    with _lock:
        _state["automation_on"] = bool(enabled)
        for p in _state["playbooks"]:
            p["enabled"] = bool(enabled)
        _state["last_message"] = "Playbook automation enabled." if enabled else "Playbook automation paused."


def set_auto_block(enabled: bool) -> None:
    with _lock:
        _state["auto_block_enabled"] = bool(enabled)
        _state["last_message"] = "Auto block enabled." if enabled else "Auto block disabled."


def set_threshold(value: int) -> None:
    v = max(40, min(95, int(value)))
    with _lock:
        _state["risk_threshold"] = v
        _state["last_message"] = f"Risk threshold set to {v}."


def toggle_playbook(playbook_id: str) -> bool | None:
    with _lock:
        for p in _state["playbooks"]:
            if p.get("id") == playbook_id:
                p["enabled"] = not bool(p.get("enabled"))
                _state["last_message"] = f"Playbook {p.get('name')} {'enabled' if p['enabled'] else 'disabled'}."
                return bool(p["enabled"])
    return None


def block_ip(ip: str, reason: str = "") -> tuple[bool, str]:
    ip = (ip or "").strip()
    if not ip or ip == "unknown":
        return False, "Invalid IP."
    with _lock:
        blocked: list[str] = _state["blocked_ips"]
        if ip in blocked:
            msg = f"IP {ip} is already blocked."
            _state["last_message"] = msg
            return False, msg
        blocked.append(ip)
        _state["blocked_ips"] = blocked
        msg = f"Blocked {ip}" + (f" ({reason})." if reason else ".")
        _state["last_message"] = msg
        return True, msg


def run_auto_block() -> tuple[list[str], str]:
    with _lock:
        if not _state["automation_on"] or not _state["auto_block_enabled"]:
            msg = "Enable automation and auto-block first."
            _state["last_message"] = msg
            return [], msg
        threshold = int(_state["risk_threshold"])
        blocked: list[str] = list(_state["blocked_ips"])

    alerts = get_alerts()
    # One row per IP with highest risk (avoid duplicate IPs from repeated alerts)
    best_by_ip: dict[str, int] = {}
    for a in alerts:
        ip = (a.get("ip") or a.get("ip_address") or "").strip()
        if not ip or ip == "unknown":
            continue
        score = _alert_risk_score(a)
        if score >= threshold:
            best_by_ip[ip] = max(best_by_ip.get(ip, 0), score)
    candidates = sorted(best_by_ip.items(), key=lambda x: x[1], reverse=True)[:6]

    to_add = [ip for ip, _ in candidates if ip not in blocked]
    if not candidates:
        msg = "No IPs crossed the selected risk threshold."
        set_message(msg)
        return [], msg
    if not to_add:
        msg = "All risky candidate IPs are already blocked."
        set_message(msg)
        return [], msg

    with _lock:
        for ip in to_add:
            if ip not in _state["blocked_ips"]:
                _state["blocked_ips"].append(ip)
        msg = f"Auto-blocked {len(to_add)} risky IP{'s' if len(to_add) != 1 else ''}."
        _state["last_message"] = msg

    return to_add, msg
