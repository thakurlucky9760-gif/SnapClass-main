"""
Time and timezone utility functions for SnapClass.
Ensures attendance records are saved with accurate UTC timestamps and
displayed in the user's local timezone (defaults to Asia/Kolkata / IST, UTC+05:30).
"""

from datetime import datetime, timezone, timedelta
from typing import Optional, Union, Any

try:
    import zoneinfo
except ImportError:
    zoneinfo = None

TIMEZONE_PRESETS = {
    "Asia/Kolkata (IST, +5:30)": "Asia/Kolkata",
    "Device / Local System": "local",
    "UTC (+00:00)": "UTC",
    "America/New_York (EST/EDT)": "America/New_York",
    "America/Los_Angeles (PST/PDT)": "America/Los_Angeles",
    "Europe/London (GMT/BST)": "Europe/London",
    "Asia/Dubai (GST, +4:00)": "Asia/Dubai",
    "Asia/Singapore (SGT, +8:00)": "Asia/Singapore",
}

DEFAULT_TIMEZONE_LABEL = "Asia/Kolkata (IST, +5:30)"


def get_available_timezones() -> list[str]:
    """Returns list of user-friendly timezone labels."""
    return list(TIMEZONE_PRESETS.keys())


def get_timezone_obj(tz_choice: str = DEFAULT_TIMEZONE_LABEL) -> Any:
    """
    Returns a timezone object based on the given label or timezone key.
    Defaults to Asia/Kolkata (IST, UTC+05:30).
    """
    tz_key = TIMEZONE_PRESETS.get(tz_choice, tz_choice)

    if tz_key == "local":
        local_tz = datetime.now().astimezone().tzinfo
        # If local system is UTC (e.g. Streamlit cloud), fall back to IST default
        if local_tz is None or getattr(local_tz, "zone", "") == "UTC" or str(local_tz) == "UTC":
            return get_timezone_obj(DEFAULT_TIMEZONE_LABEL)
        return local_tz

    if tz_key == "UTC":
        return timezone.utc

    if zoneinfo is not None:
        try:
            return zoneinfo.ZoneInfo(tz_key)
        except Exception:
            pass

    # Standard library fallback offsets
    if tz_key == "Asia/Kolkata":
        return timezone(timedelta(hours=5, minutes=30), name="IST")
    if tz_key == "Asia/Dubai":
        return timezone(timedelta(hours=4), name="GST")
    if tz_key == "Asia/Singapore":
        return timezone(timedelta(hours=8), name="SGT")
    if tz_key == "America/New_York":
        return timezone(timedelta(hours=-5), name="EST")
    if tz_key == "America/Los_Angeles":
        return timezone(timedelta(hours=-8), name="PST")
    if tz_key == "Europe/London":
        return timezone(timedelta(hours=0), name="GMT")

    return timezone(timedelta(hours=5, minutes=30), name="IST")


def get_current_utc_iso() -> str:
    """
    Returns current time in ISO-8601 UTC format with explicit timezone.
    Guarantees consistency across local development, servers, and cloud hosts.
    Example: '2026-10-24T16:08:20+00:00'
    """
    return datetime.now(timezone.utc).isoformat()


def parse_timestamp(ts: Union[str, datetime, None]) -> Optional[datetime]:
    """
    Parses a timestamp string or object into a timezone-aware UTC datetime.
    Handles ISO format, 'Z' suffix, microseconds, or naive datetimes.
    """
    if ts is None:
        return None
    if isinstance(ts, datetime):
        if ts.tzinfo is None:
            return ts.replace(tzinfo=timezone.utc)
        return ts.astimezone(timezone.utc)

    ts_str = str(ts).strip()
    if not ts_str:
        return None

    # Replace 'Z' with '+00:00'
    ts_clean = ts_str.replace("Z", "+00:00")
    try:
        dt = datetime.fromisoformat(ts_clean)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except Exception:
        # Fallback parsing
        try:
            parts = ts_clean.split("T")
            if len(parts) == 2:
                date_part, time_part = parts
                time_clean = time_part.split("+")[0].split("-")[0]
                dt = datetime.strptime(f"{date_part} {time_clean[:8]}", "%Y-%m-%d %H:%M:%S")
                return dt.replace(tzinfo=timezone.utc)
        except Exception:
            pass
        return None


def format_timestamp(
    ts: Union[str, datetime, None],
    tz_choice: str = DEFAULT_TIMEZONE_LABEL,
    format_str: str = "%Y-%m-%d %I:%M %p"
) -> str:
    """
    Formats a timestamp for display in the target timezone.
    Default format produces strings like '2026-10-24 09:27 PM'.
    """
    dt_utc = parse_timestamp(ts)
    if dt_utc is None:
        return "N/A"

    tz_obj = get_timezone_obj(tz_choice)
    dt_local = dt_utc.astimezone(tz_obj)
    return dt_local.strftime(format_str)
