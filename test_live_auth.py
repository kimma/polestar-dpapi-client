#!/usr/bin/env python3
"""Live test program for Polestar API authentication, vehicles, and telemetry."""

import sys
import json
from pathlib import Path
from dataclasses import asdict, is_dataclass
from datetime import datetime, timezone

sys.path.insert(0, ".")

from polestar_dpapi_client import PolestarClient, AuthenticationError, ApiRequestError


# ---------------------------------------------------------------------------
# ANSI colour helpers
# ---------------------------------------------------------------------------

class C:
    """ANSI colour codes for terminal output."""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"

    # Colours
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    # Bright colours
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"


def _coloured_value(value):
    """Return a coloured string representation of a value based on its type."""
    if value is None:
        return f"{C.DIM}{C.RED}None{C.RESET}"
    if isinstance(value, bool):
        colour = C.BRIGHT_GREEN if value else C.BRIGHT_YELLOW
        return f"{colour}{str(value)}{C.RESET}"
    if isinstance(value, (int, float)):
        return f"{C.CYAN}{value}{C.RESET}"
    if isinstance(value, str):
        return f'{C.GREEN}"{value}"{C.RESET}'
    if isinstance(value, list):
        if not value:
            return f"{C.DIM}[]{C.RESET}"
        return f"{C.DIM}[{len(value)} items]{C.RESET}"
    if is_dataclass(value):
        d = asdict(value)
        return f"{C.DIM}{{object: {len(d)} fields}}{C.RESET}"
    return f"{C.WHITE}{value}{C.RESET}"


def _coloured_key(key):
    """Return a coloured key string."""
    return f"{C.BOLD}{C.MAGENTA}{key}{C.RESET}"


# ---------------------------------------------------------------------------
# Credentials
# ---------------------------------------------------------------------------


def _load_credentials():
    """Load credentials from credentials.json in the same directory as this script."""
    script_dir = Path(__file__).parent
    credentials_path = script_dir / "credentials.json"
    if not credentials_path.exists():
        print(f"Error: Credentials file not found at {credentials_path}")
        print("  Please create a credentials.json file with the following structure:")
        print('  {"client_id": "...", "client_secret": "...", "base_url": "..."}')
        sys.exit(1)
    with open(credentials_path, "r") as f:
        return json.load(f)


CREDENTIALS = _load_credentials()
CLIENT_ID = CREDENTIALS["client_id"]
CLIENT_SECRET = CREDENTIALS["client_secret"]
BASE_URL = CREDENTIALS["base_url"]
CLIENT_HEADER_ID = CREDENTIALS["client_header_id"]


# ---------------------------------------------------------------------------
# Telemetry endpoints
# ---------------------------------------------------------------------------

TELEMETRY_ENDPOINTS = [
    ("Availability", "get_availability"),
    ("Battery", "get_battery"),
    ("Exterior", "get_exterior"),
    ("Health", "get_health"),
    ("Location", "get_location"),
    ("Odometer", "get_odometer"),
    ("Parking Climatization", "get_parking_climatization"),
    ("Pre-Cleaning", "get_pre_cleaning"),
]

# ---------------------------------------------------------------------------
# Charging endpoints
# ---------------------------------------------------------------------------

CHARGING_ENDPOINTS = [
    ("Amp Limit", "get_amp_limit"),
    ("Charge Locations", "get_charge_locations"),
    ("Charge Now", "get_charge_now"),
    ("Global Charge Timer", "get_global_charge_timer"),
    ("Is At Charge Location", "get_is_at_charge_location"),
    ("Parking Climate Timer", "get_parking_climate_timer"),
    ("Target SoC", "get_target_soc"),
]

TELEMETRY_SCOPE = (
    "pdp-telemetry/availability pdp-telemetry/battery pdp-telemetry/exterior "
    "pdp-telemetry/health pdp-telemetry/location pdp-telemetry/odometer "
    "pdp-telemetry/parkingClimatization pdp-telemetry/preCleaning "
    "pdp-charging/ampLimit pdp-charging/chargeLocations "
    "pdp-charging/overrideChargeTimer pdp-charging/globalChargeTimer "
    "pdp-charging/isAtChargeLocation pdp-charging/parkingClimateTimer "
    "pdp-charging/targetSoc"
)


# ---------------------------------------------------------------------------
# Display helpers
# ---------------------------------------------------------------------------


def _print_section(title):
    """Print a section header with coloured separators."""
    width = 72
    print()
    print(f"{C.BOLD}{'=' * width}{C.RESET}")
    print(f" {C.BOLD}{C.WHITE}{title}{C.RESET}")
    print(f"{C.BOLD}{'=' * width}{C.RESET}")


def _print_subsection(title):
    """Print a subsection header."""
    print(f"\n  {C.BOLD}{C.BLUE}--- {title} ---{C.RESET}")


def _print_kv(key, value):
    """Print a single key-value pair with colours."""
    print(f"    {_coloured_key(key)}: {_coloured_value(value)}")


def _print_dataclass(obj, indent: int = 4):
    """Recursively print a dataclass (or dict) with coloured values."""
    prefix = " " * indent
    if is_dataclass(obj):
        data = asdict(obj)
    elif isinstance(obj, dict):
        data = obj
    else:
        print(f"{prefix}{_coloured_value(obj)}")
        return

    for key, value in data.items():
        if is_dataclass(value) or isinstance(value, dict):
            # Nested object — print key then recurse
            print(f"{prefix}{_coloured_key(key)}:")
            _print_dataclass(value, indent + 2)
        else:
            _print_kv(key, value)


def _print_response(label, response):
    """Print the full response: both .data and .meta."""
    _print_subsection(f"{label} — Data")
    _print_dataclass(response.data)

    _print_subsection(f"{label} — Meta")
    _print_dataclass(response.meta)


def _print_raw_json(label, data_obj):
    """Fallback: pretty-print as JSON with syntax colours via coloured_value."""
    _print_subsection(label)
    try:
        data_dict = asdict(data_obj) if is_dataclass(data_obj) else data_obj
        raw = json.dumps(data_dict, indent=4, default=str)
        # Print with minimal colouring per line
        for line in raw.splitlines():
            stripped = line.strip().rstrip(",")
            if ":" in stripped:
                key_part, _, val_part = stripped.partition(":")
                print(f"    {_coloured_key(key_part.strip())}: {_coloured_value(val_part.strip())}")
            else:
                print(f"    {C.DIM}{line}{C.RESET}")
    except Exception as e:
        _print_subsection(f"{label} (print error)")
        print(f"    {C.RED}{e}{C.RESET}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    _print_section("Polestar API Live Test")
    print(f"  {_coloured_key('Client ID')}: {_coloured_value(CLIENT_ID[:8] + '...')}")
    print(f"  {_coloured_key('Base URL')}: {_coloured_value(BASE_URL)}")
    print(f"  {_coloured_key('Scope')}: {_coloured_value(TELEMETRY_SCOPE)}")
    now = datetime.now(timezone.utc)
    print(f"  {_coloured_key('UTC Time')}: {_coloured_value(now.isoformat())}")

    client = PolestarClient(
        app_client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        client_header_id=CLIENT_HEADER_ID,
        base_url=BASE_URL,
    )

    # ------------------------------------------------------------------
    # Authenticate
    # ------------------------------------------------------------------
    _print_section("Authentication")
    print(f"  Requesting access token...")
    try:
        token = client.authenticate(scope=TELEMETRY_SCOPE)
        print(f"  {C.BRIGHT_GREEN}Success!{C.RESET}")
        _print_subsection("Token Response")
        _print_kv("token_type", token.token_type)
        _print_kv("expires_in", token.expires_in)
        _print_kv("access_token", token.access_token[:20] + "...")
        _print_kv("headers", token.headers)
    except AuthenticationError as e:
        print(f"\n  {C.RED}Authentication failed:{C.RESET} {e}")
        print(f"  {_coloured_key('Status Code')}: {_coloured_value(e.status_code)}")
        sys.exit(1)
    except ApiRequestError as e:
        print(f"\n  {C.RED}API request failed:{C.RESET} {e}")
        print(f"  {_coloured_key('Status Code')}: {_coloured_value(e.status_code)}")
        sys.exit(1)

    # ------------------------------------------------------------------
    # List Vehicles
    # ------------------------------------------------------------------
    _print_section("Vehicles")
    try:
        print(f"  Requesting vehicles list...")
        vehicles = client.list_vehicles()
        print(f"  {C.BRIGHT_GREEN}Success!{C.RESET}")
        _print_subsection("Vehicles Response — Data")
        _print_kv("count", vehicles.meta.count)
        _print_kv("vins", vehicles.data)
    except AuthenticationError as e:
        print(f"\n  {C.RED}Vehicles authentication failed:{C.RESET} {e}")
        print(f"  {_coloured_key('Status Code')}: {_coloured_value(e.status_code)}")
        sys.exit(1)
    except ApiRequestError as e:
        print(f"\n  {C.RED}Vehicles API request failed:{C.RESET} {e}")
        print(f"  {_coloured_key('Status Code')}: {_coloured_value(e.status_code)}")
        sys.exit(1)

    if not vehicles.data:
        print(f"\n  {C.YELLOW}No vehicles found. Exiting.{C.RESET}")
        return

    # ------------------------------------------------------------------
    # Fetch Telemetry for Each Vehicle
    # ------------------------------------------------------------------
    for vin in vehicles.data:
        _print_section(f"Telemetry for VIN: {vin}")

        for display_name, method_name in TELEMETRY_ENDPOINTS:
            print(f"\n  Fetching {C.BOLD}{display_name}{C.RESET}...")
            try:
                method = getattr(client, method_name)
                result = method(vin)
                _print_response(display_name, result)
            except ApiRequestError as e:
                print(f"    {C.RED}FAILED:{C.RESET} {e}")
                print(f"    {_coloured_key('Status Code')}: {_coloured_value(e.status_code)}")
            except Exception as e:
                print(f"    {C.RED}UNEXPECTED ERROR:{C.RESET} {e}")

        # ------------------------------------------------------------------
        # Fetch Charging for Each Vehicle
        # ------------------------------------------------------------------
        _print_section(f"Charging for VIN: {vin}")

        for display_name, method_name in CHARGING_ENDPOINTS:
            print(f"\n  Fetching {C.BOLD}{display_name}{C.RESET}...")
            try:
                method = getattr(client, method_name)
                result = method(vin)
                _print_response(display_name, result)
            except ApiRequestError as e:
                print(f"    {C.RED}FAILED:{C.RESET} {e}")
                print(f"    {_coloured_key('Status Code')}: {_coloured_value(e.status_code)}")
            except Exception as e:
                print(f"    {C.RED}UNEXPECTED ERROR:{C.RESET} {e}")

    # ------------------------------------------------------------------
    # Done
    # ------------------------------------------------------------------
    _print_section("Complete")
    print(f"  {C.BRIGHT_GREEN}All telemetry fetches completed.{C.RESET}")


if __name__ == "__main__":
    main()
