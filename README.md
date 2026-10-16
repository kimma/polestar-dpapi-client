# Polestar DPAPI Client

A Python client library for interfacing with the Polestar M2M (machine-to-machine) data platform API. It provides typed access to vehicle telemetry (battery, location, health, exterior, odometer, availability, parking climatization, pre-cleaning) and charging state (amp limit, charge locations, charge timers, target SoC).

## AI Usage

This project was 100% coded by a local LLM.  
I got bored waiting for WoW: Forever to launch, and i had just bought a Polestar, so i figured i'd look into LLMs and also do something useful - fetch statistical data from the car.  
First step: make a module, to utilize in the data gathering backend.


## Features

- OAuth2 client-credentials authentication against the Polestar M2M API
- Typed dataclass models for all telemetry and charging responses
- Vehicle listing with delegated account support
- Structured exception hierarchy for error handling
- Python 3.10+ with type hints throughout

## Requirements

- Python 3.10 or later
- A Polestar developer portal account with M2M API credentials (`app_client_id`, `client_secret`, and `client_header_id`)

## Installation

```bash
pip install polestar-dpapi-client
```

### Development installation

```bash
# Clone the repository
git clone https://github.com/kimma/polestar-dpapi-client.git
cd polestar-dpapi-client

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate

# Install with dev dependencies
pip install -e ".[dev]"
```

## Quick Start

```python
from polestar_dpapi_client import PolestarClient

# Create a client with your developer portal credentials
client = PolestarClient(
    app_client_id="your_client_id",
    client_secret="your_client_secret",
    client_header_id="your_client_header_id",
)

# Authenticate to obtain an access token
token = client.authenticate()
print(token.access_token, token.expires_in)

# List vehicles you are authorized to access
vehicles = client.list_vehicles()
print(vehicles.data)

# Fetch telemetry for a specific vehicle
vin = vehicles.data[0]
battery = client.get_battery(vin)
print(battery.state.charge_level)
```

## Usage

### Authentication

Call [`authenticate()`](polestar_dpapi_client/api/client.py:76) once per session. The token is cached on the client and reused by subsequent requests.

```python
token = client.authenticate(scope="pdp-telemetry/battery pdp-telemetry/location")
```

Supported scopes include:

- `pdp-telemetry/availability`, `pdp-telemetry/battery`, `pdp-telemetry/exterior`, `pdp-telemetry/health`, `pdp-telemetry/location`, `pdp-telemetry/odometer`, `pdp-telemetry/parkingClimatization`, `pdp-telemetry/preCleaning`
- `pdp-charging/ampLimit`, `pdp-charging/chargeLocations`, `pdp-charging/overrideChargeTimer`, `pdp-charging/globalChargeTimer`, `pdp-charging/isAtChargeLocation`, `pdp-charging/parkingClimateTimer`, `pdp-charging/targetSoc`

### Telemetry endpoints

| Method | Description |
| --- | --- |
| [`get_availability(vin)`](polestar_dpapi_client/api/client.py:315) | Availability status, usage mode, unavailability reason |
| [`get_battery(vin)`](polestar_dpapi_client/api/client.py:341) | Charge level, charging status, range, energy consumption |
| [`get_exterior(vin)`](polestar_dpapi_client/api/client.py:368) | Doors, locks, windows, hood, trunk status |
| [`get_health(vin)`](polestar_dpapi_client/api/client.py:394) | Service warnings, trip meters, fluid levels, light warnings |
| [`get_location(vin)`](polestar_dpapi_client/api/client.py:421) | Latitude, longitude, altitude, heading, speed |
| [`get_odometer(vin)`](polestar_dpapi_client/api/client.py:447) | Total odometer, trip meters, average speed |
| [`get_parking_climatization(vin)`](polestar_dpapi_client/api/client.py:473) | Running status, temperatures, seat heating, timers |
| [`get_pre_cleaning(vin)`](polestar_dpapi_client/api/client.py:500) | Air quality index, PM2.5, running status, cycle info |

### Charging endpoints

| Method | Description |
| --- | --- |
| [`get_amp_limit(vin)`](polestar_dpapi_client/api/client.py:530) | Configured and pending amp limit |
| [`get_charge_locations(vin)`](polestar_dpapi_client/api/client.py:556) | Configured charge locations and deletion queue |
| [`get_charge_now(vin)`](polestar_dpapi_client/api/client.py:582) | Override charge timer status |
| [`get_global_charge_timer(vin)`](polestar_dpapi_client/api/client.py:608) | Global charge timer configuration |
| [`get_is_at_charge_location(vin)`](polestar_dpapi_client/api/client.py:634) | Whether the vehicle is at a charge location |
| [`get_parking_climate_timer(vin)`](polestar_dpapi_client/api/client.py:660) | Parking climate timers and settings |
| [`get_target_soc(vin)`](polestar_dpapi_client/api/client.py:686) | Target state of charge configuration |

All methods accept an optional `delegated_account_id` argument for third-party credentials accessing shared VINs.

### Error handling

The library raises a structured exception hierarchy rooted at [`PolestarAPIError`](polestar_dpapi_client/exceptions.py:4):

```python
from polestar_dpapi_client import PolestarClient, AuthenticationError, ApiRequestError

try:
    client.authenticate()
    battery = client.get_battery(vin)
except AuthenticationError as exc:
    print(f"Authentication failed: {exc}")
except ApiRequestError as exc:
    print(f"API request failed (HTTP {exc.status_code}): {exc}")
```

- `AuthenticationError` — invalid credentials, missing token, or identity provider rejection
- `ApiRequestError` — network failures, rate limiting (429), or other API errors; includes `status_code` when available

## Project Structure

```
polestar_dpapi_client/
├── __init__.py          # Public API exports
├── exceptions.py        # Exception hierarchy
├── api/
│   └── client.py        # PolestarClient HTTP client
├── models/
│   ├── token.py         # TokenResponse
│   ├── vehicles.py      # VehiclesListResponse, VehiclesMeta
│   ├── telemetry.py     # Telemetry response models
│   └── charging.py      # Charging response models
└── utils/
    └── telemetry_parser.py  # Response parsing helpers
tests/                   # pytest test suite
```

## Development

```bash
# Install with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run tests with coverage
pytest --cov=polestar_dpapi_client

# Lint and format
ruff check .
black .
```

## Versioning

This project follows [Semantic Versioning](https://semver.org/). The current version is `1.0.1`.

## License

Distributed under the MIT License. See [pyproject.toml](pyproject.toml:10) for details.

## Contributing

Contributions are welcome. Please open an issue or pull request on the [repository](https://github.com/kimma/polestar-dpapi-client).

## Links

- **Repository:** <https://github.com/kimma/polestar-dpapi-client>
- **Bug Tracker:** <https://github.com/kimma/polestar-dpapi-client/issues>
