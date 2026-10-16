"""Tests for the Polestar API telemetry endpoints."""

from unittest.mock import MagicMock, patch

import pytest
import requests

from polestar_dpapi_client import (
    PolestarClient,
    TokenResponse,
    AvailabilityTelemetryResponse,
    AvailabilityState,
    BatteryTelemetryResponse,
    BatteryState,
    ExteriorTelemetryResponse,
    ExteriorState,
    HealthTelemetryResponse,
    HealthState,
    LocationTelemetryResponse,
    LocationState,
    OdometerTelemetryResponse,
    OdometerState,
    ParkingClimatizationTelemetryResponse,
    ParkingClimatizationState,
    PreCleaningTelemetryResponse,
    PreCleaningState,
    TelemetryMeta,
    TelemetryTimestamp,
    TelemetryCoordinate,
    AuthenticationError,
    ApiRequestError,
)


def _make_client() -> PolestarClient:
    client = PolestarClient(app_client_id="my_id", client_secret="my_secret", client_header_id="my_header")
    client._token = TokenResponse(
        access_token="test-token",
        expires_in=3600,
        token_type="Bearer",
    )
    return client


# ---------------------------------------------------------------------------
# Availability
# ---------------------------------------------------------------------------


class TestGetAvailability:
    @patch("requests.Session.get")
    def test_successful_availability(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "vin": "YV1CZ000000000001",
                "timestamp": {"seconds": "1700000000", "nanos": 0},
                "availabilityStatus": "AVAILABILITY_STATUS_AVAILABLE",
                "unavailableReason": None,
                "usageMode": "USAGE_MODE_INACTIVE",
                "metaReceivedAt": "2024-01-15T10:00:00Z",
                "metaEventId": "evt-123",
            },
            "meta": {"vin": "YV1CZ000000000001", "domain": "availability"},
        }
        mock_get.return_value = mock_response

        client = _make_client()
        result = client.get_availability("YV1CZ000000000001")

        assert isinstance(result, AvailabilityTelemetryResponse)
        assert isinstance(result.data, AvailabilityState)
        assert result.data.vin == "YV1CZ000000000001"
        assert result.data.availability_status == "AVAILABILITY_STATUS_AVAILABLE"
        assert result.data.usage_mode == "USAGE_MODE_INACTIVE"
        assert isinstance(result.data.timestamp, TelemetryTimestamp)
        assert result.data.timestamp.seconds == "1700000000"
        assert isinstance(result.meta, TelemetryMeta)
        assert result.meta.domain == "availability"

    @patch("requests.Session.get")
    def test_availability_sends_correct_headers(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {"vin": "YV1CZ000000000001"},
            "meta": {"vin": "YV1CZ000000000001", "domain": "availability"},
        }
        mock_get.return_value = mock_response

        client = _make_client()
        client.get_availability("YV1CZ000000000001")

        call_kwargs = mock_get.call_args[1]
        headers = call_kwargs["headers"]
        assert headers["Authorization"] == "Bearer test-token"
        assert headers["x-client-id"] == "my_header"
        assert "YV1CZ000000000001" in mock_get.call_args[0][0]


# ---------------------------------------------------------------------------
# Battery
# ---------------------------------------------------------------------------


class TestGetBattery:
    @patch("requests.Session.get")
    def test_successful_battery(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "vin": "YV1CZ000000000001",
                "timestamp": {"seconds": "1700000000", "nanos": 0},
                "batteryChargeLevelPercentage": 75,
                "chargingStatusV2": "CHARGING_STATUS_V2_IDLE",
                "chargingType": "CHARGING_TYPE_AC",
                "estimatedDistanceToEmptyKm": 320.5,
                "estimatedChargingTimeToFullMinutes": None,
                "metaReceivedAt": "2024-01-15T10:00:00Z",
                "metaEventId": "evt-456",
            },
            "meta": {"vin": "YV1CZ000000000001", "domain": "battery"},
        }
        mock_get.return_value = mock_response

        client = _make_client()
        result = client.get_battery("YV1CZ000000000001")

        assert isinstance(result, BatteryTelemetryResponse)
        assert isinstance(result.data, BatteryState)
        assert result.data.battery_charge_level_percentage == 75
        assert result.data.charging_status_v2 == "CHARGING_STATUS_V2_IDLE"
        assert result.data.charging_type == "CHARGING_TYPE_AC"
        assert result.data.estimated_distance_to_empty_km == 320.5

    @patch("requests.Session.get")
    def test_battery_with_nested_objects(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "vin": "YV1CZ000000000001",
                "dischargeInfo": {
                    "energyAvailable": 50.0,
                    "energyAvailableIncrease": 5.0,
                    "powerLimit": 11000,
                },
                "energyConsumptionPercentageManual": {
                    "driving": 60.0,
                    "climate": 20.0,
                    "battery": 10.0,
                    "other": 10.0,
                },
                "manualPreconditioning": {
                    "preconditioningStatus": "MANUAL_PRECONDITIONING_STATUS_OFF",
                },
            },
            "meta": {"vin": "YV1CZ000000000001", "domain": "battery"},
        }
        mock_get.return_value = mock_response

        client = _make_client()
        result = client.get_battery("YV1CZ000000000001")

        assert result.data.discharge_info is not None
        assert result.data.discharge_info.energy_available == 50.0
        assert result.data.energy_consumption_percentage_manual is not None
        assert result.data.energy_consumption_percentage_manual.driving == 60.0
        assert result.data.manual_preconditioning is not None


# ---------------------------------------------------------------------------
# Exterior
# ---------------------------------------------------------------------------


class TestGetExterior:
    @patch("requests.Session.get")
    def test_successful_exterior(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "vin": "YV1CZ000000000001",
                "centralLock": "LOCK_STATUS_LOCKED",
                "frontLeftDoor": "OPEN_STATUS_CLOSED",
                "frontRightDoor": "OPEN_STATUS_CLOSED",
                "hood": "OPEN_STATUS_CLOSED",
                "trunk": "OPEN_STATUS_CLOSED",
            },
            "meta": {"vin": "YV1CZ000000000001", "domain": "exterior"},
        }
        mock_get.return_value = mock_response

        client = _make_client()
        result = client.get_exterior("YV1CZ000000000001")

        assert isinstance(result, ExteriorTelemetryResponse)
        assert isinstance(result.data, ExteriorState)
        assert result.data.central_lock == "LOCK_STATUS_LOCKED"
        assert result.data.front_left_door == "OPEN_STATUS_CLOSED"
        assert result.data.hood == "OPEN_STATUS_CLOSED"


# ---------------------------------------------------------------------------
# Health
# ---------------------------------------------------------------------------


class TestGetHealth:
    @patch("requests.Session.get")
    def test_successful_health(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "vin": "YV1CZ000000000001",
                "lowVoltageBatteryWarning": "LOW_VOLTAGE_BATTERY_WARNING_NO_WARNING",
                "distanceToServiceKm": 5000,
            },
            "meta": {"vin": "YV1CZ000000000001", "domain": "health"},
        }
        mock_get.return_value = mock_response

        client = _make_client()
        result = client.get_health("YV1CZ000000000001")

        assert isinstance(result, HealthTelemetryResponse)
        assert isinstance(result.data, HealthState)
        assert result.data.low_voltage_battery_warning == "LOW_VOLTAGE_BATTERY_WARNING_NO_WARNING"
        assert result.data.distance_to_service_km == 5000


# ---------------------------------------------------------------------------
# Location
# ---------------------------------------------------------------------------


class TestGetLocation:
    @patch("requests.Session.get")
    def test_successful_location(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "vin": "YV1CZ000000000001",
                "coordinate": {
                    "latitude": 59.3293,
                    "longitude": 18.0686,
                },
                "altitude": "30",
                "heading": 180,
                "speed": "0",
            },
            "meta": {"vin": "YV1CZ000000000001", "domain": "location"},
        }
        mock_get.return_value = mock_response

        client = _make_client()
        result = client.get_location("YV1CZ000000000001")

        assert isinstance(result, LocationTelemetryResponse)
        assert isinstance(result.data, LocationState)
        assert isinstance(result.data.coordinate, TelemetryCoordinate)
        assert result.data.coordinate.latitude == 59.3293
        assert result.data.coordinate.longitude == 18.0686
        assert result.data.altitude == "30"
        assert result.data.heading == 180


# ---------------------------------------------------------------------------
# Odometer
# ---------------------------------------------------------------------------


class TestGetOdometer:
    @patch("requests.Session.get")
    def test_successful_odometer(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "vin": "YV1CZ000000000001",
                "odometerMeters": 50000000,
                "tripMeterManualKm": 120.5,
                "averageSpeedKmPerHour": 65.3,
            },
            "meta": {"vin": "YV1CZ000000000001", "domain": "odometer"},
        }
        mock_get.return_value = mock_response

        client = _make_client()
        result = client.get_odometer("YV1CZ000000000001")

        assert isinstance(result, OdometerTelemetryResponse)
        assert isinstance(result.data, OdometerState)
        assert result.data.odometer_meters == 50000000
        assert result.data.trip_meter_manual_km == 120.5
        assert result.data.average_speed_km_per_hour == 65.3


# ---------------------------------------------------------------------------
# Parking Climatization
# ---------------------------------------------------------------------------


class TestGetParkingClimatization:
    @patch("requests.Session.get")
    def test_successful_parking_climatization(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "vin": "YV1CZ000000000001",
                "runningStatus": "RUNNING_STATUS_OFF",
                "ventilation": "VENTILATION_NEUTRAL",
                "currentCompartmentTemperatureCelsius": 21.0,
                "requestedCompartmentTemperatureCelsius": 22.0,
            },
            "meta": {"vin": "YV1CZ000000000001", "domain": "parkingClimatization"},
        }
        mock_get.return_value = mock_response

        client = _make_client()
        result = client.get_parking_climatization("YV1CZ000000000001")

        assert isinstance(result, ParkingClimatizationTelemetryResponse)
        assert isinstance(result.data, ParkingClimatizationState)
        assert result.data.running_status == "RUNNING_STATUS_OFF"
        assert result.data.ventilation == "VENTILATION_NEUTRAL"
        assert result.data.current_compartment_temperature_celsius == 21.0


# ---------------------------------------------------------------------------
# Pre-Cleaning
# ---------------------------------------------------------------------------


class TestGetPreCleaning:
    @patch("requests.Session.get")
    def test_successful_pre_cleaning(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {
                "vin": "YV1CZ000000000001",
                "runningStatus": "RUNNING_STATUS_OFF",
                "measuredAirQualityIndex": 42,
                "measuredParticulateMatter25": 10.5,
                "lastCycleValid": True,
            },
            "meta": {"vin": "YV1CZ000000000001", "domain": "preCleaning"},
        }
        mock_get.return_value = mock_response

        client = _make_client()
        result = client.get_pre_cleaning("YV1CZ000000000001")

        assert isinstance(result, PreCleaningTelemetryResponse)
        assert isinstance(result.data, PreCleaningState)
        assert result.data.running_status == "RUNNING_STATUS_OFF"
        assert result.data.measured_air_quality_index == 42
        assert result.data.measured_particulate_matter_25 == 10.5
        assert result.data.last_cycle_valid is True


# ---------------------------------------------------------------------------
# Shared error / auth tests
# ---------------------------------------------------------------------------


class TestTelemetryAuth:
    def test_raises_without_token(self):
        client = PolestarClient(app_client_id="my_id", client_secret="my_secret", client_header_id="my_header")
        with pytest.raises(AuthenticationError, match="No access token available"):
            client.get_availability("YV1CZ000000000001")

    @patch("requests.Session.get")
    def test_404_raises_api_request_error(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.json.return_value = {
            "error": {
                "code": "NOT_FOUND",
                "message": "Vehicle not found",
                "httpStatus": 404,
                "timestamp": "2024-01-01T00:00:00Z",
            },
        }
        mock_get.return_value = mock_response

        client = _make_client()
        with pytest.raises(ApiRequestError, match="not found"):
            client.get_battery("INVALID_VIN")

    @patch("requests.Session.get")
    def test_429_raises_api_request_error(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 429
        mock_response.json.return_value = {
            "error": {
                "code": "RATE_LIMITED",
                "message": "Too many requests",
                "httpStatus": 429,
                "timestamp": "2024-01-01T00:00:00Z",
            },
        }
        mock_get.return_value = mock_response

        client = _make_client()
        with pytest.raises(ApiRequestError, match="Rate limit"):
            client.get_location("YV1CZ000000000001")

    @patch("requests.Session.get")
    def test_connection_error_raises_api_request_error(self, mock_get):
        mock_get.side_effect = requests.ConnectionError("Network unreachable")

        client = _make_client()
        with pytest.raises(ApiRequestError, match="Failed to connect"):
            client.get_odometer("YV1CZ000000000001")

    @patch("requests.Session.get")
    def test_delegated_account_id_header(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {"vin": "YV1CZ000000000001"},
            "meta": {"vin": "YV1CZ000000000001", "domain": "availability"},
        }
        mock_get.return_value = mock_response

        client = _make_client()
        client.get_availability(
            "YV1CZ000000000001",
            delegated_account_id="jane.doe@acme.com",
        )

        call_kwargs = mock_get.call_args[1]
        headers = call_kwargs["headers"]
        assert headers["x-delegated-account-id"] == "jane.doe@acme.com"
