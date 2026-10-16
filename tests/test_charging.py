"""Tests for the Polestar API charging models and parsers."""

import pytest

from polestar_dpapi_client.models.charging import (
    ChargingMeta,
    ChargingTimestamp,
    ChargingCoordinate,
    AmpLimitValue,
    AmpLimitState,
    AmpLimitTelemetryResponse,
    ChargeTimer,
    ChargeLocation,
    ChargeLocationsState,
    ChargeLocationsTelemetryResponse,
    OverrideChargeTimerValue,
    ChargeNowState,
    ChargeNowTelemetryResponse,
    GlobalChargeTimerValue,
    GlobalChargeTimerState,
    GlobalChargeTimerTelemetryResponse,
    IsAtChargeLocationState,
    IsAtChargeLocationResponse,
    TimerSettings,
    ParkingClimateTimer,
    ParkingClimateTimerState,
    ParkingClimateTimerTelemetryResponse,
    TargetSocValue,
    TargetSocState,
    TargetSocTelemetryResponse,
)
from polestar_dpapi_client.utils.telemetry_parser import (
    parse_amp_limit_response,
    parse_charge_locations_response,
    parse_charge_now_response,
    parse_global_charge_timer_response,
    parse_is_at_charge_location_response,
    parse_parking_climate_timer_response,
    parse_target_soc_response,
)


# ---------------------------------------------------------------------------
# Shared types - dataclass tests
# ---------------------------------------------------------------------------


class TestChargingMeta:
    def test_creation(self):
        meta = ChargingMeta(vin="YV1CZ000000000001", domain="ampLimit")
        assert meta.vin == "YV1CZ000000000001"
        assert meta.domain == "ampLimit"


class TestChargingTimestamp:
    def test_creation_with_values(self):
        ts = ChargingTimestamp(seconds="1700000000", nanos=123456789)
        assert ts.seconds == "1700000000"
        assert ts.nanos == 123456789

    def test_defaults_to_none(self):
        ts = ChargingTimestamp()
        assert ts.seconds is None
        assert ts.nanos is None


class TestChargingCoordinate:
    def test_creation_with_values(self):
        coord = ChargingCoordinate(latitude=59.3293, longitude=18.0686)
        assert coord.latitude == 59.3293
        assert coord.longitude == 18.0686

    def test_defaults_to_none(self):
        coord = ChargingCoordinate()
        assert coord.latitude is None
        assert coord.longitude is None


# ---------------------------------------------------------------------------
# Amp Limit - dataclass tests
# ---------------------------------------------------------------------------


class TestAmpLimitValue:
    def test_creation_with_values(self):
        val = AmpLimitValue(
            amp_limit=16.0,
            updated_at="2024-01-15T10:00:00Z",
            updated_at_timestamp=ChargingTimestamp(seconds="1700000000", nanos=0),
            source="app",
            id="amp-limit-1",
        )
        assert val.amp_limit == 16.0
        assert val.source == "app"
        assert val.id == "amp-limit-1"
        assert isinstance(val.updated_at_timestamp, ChargingTimestamp)

    def test_defaults_to_none(self):
        val = AmpLimitValue()
        assert val.amp_limit is None
        assert val.updated_at is None
        assert val.updated_at_timestamp is None
        assert val.source is None
        assert val.id is None


class TestAmpLimitState:
    def test_creation_with_values(self):
        state = AmpLimitState(
            vin="YV1CZ000000000001",
            id="state-1",
            amp_limit=AmpLimitValue(amp_limit=16.0),
            pending_amp_limit=AmpLimitValue(amp_limit=12.0),
        )
        assert state.vin == "YV1CZ000000000001"
        assert state.amp_limit.amp_limit == 16.0
        assert state.pending_amp_limit.amp_limit == 12.0

    def test_vin_required(self):
        state = AmpLimitState(vin="YV1CZ000000000001")
        assert state.vin == "YV1CZ000000000001"
        assert state.amp_limit is None


class TestAmpLimitTelemetryResponse:
    def test_creation(self):
        response = AmpLimitTelemetryResponse(
            data=AmpLimitState(vin="YV1CZ000000000001"),
            meta=ChargingMeta(vin="YV1CZ000000000001", domain="ampLimit"),
        )
        assert isinstance(response.data, AmpLimitState)
        assert isinstance(response.meta, ChargingMeta)
        assert response.meta.domain == "ampLimit"


# ---------------------------------------------------------------------------
# Amp Limit - parser tests
# ---------------------------------------------------------------------------


class TestParseAmpLimitResponse:
    def test_full_response(self):
        data = {
            "data": {
                "vin": "YV1CZ000000000001",
                "id": "state-1",
                "updatedAt": "2024-01-15T10:00:00Z",
                "updatedAtTimestamp": {"seconds": "1700000000", "nanos": 0},
                "ampLimit": {
                    "ampLimit": 16.0,
                    "updatedAt": "2024-01-15T10:00:00Z",
                    "updatedAtTimestamp": {"seconds": "1700000000", "nanos": 0},
                    "source": "app",
                    "id": "amp-limit-1",
                },
                "pendingAmpLimit": {
                    "ampLimit": 12.0,
                    "source": "app",
                    "id": "amp-limit-2",
                },
                "metaReceivedAt": "2024-01-15T10:00:00Z",
                "metaEventId": "evt-123",
            },
            "meta": {"vin": "YV1CZ000000000001", "domain": "ampLimit"},
        }
        result = parse_amp_limit_response(data)
        assert isinstance(result, AmpLimitTelemetryResponse)
        assert result.data.vin == "YV1CZ000000000001"
        assert result.data.id == "state-1"
        assert result.data.amp_limit.amp_limit == 16.0
        assert result.data.amp_limit.source == "app"
        assert result.data.pending_amp_limit.amp_limit == 12.0
        assert isinstance(result.data.updated_at_timestamp, ChargingTimestamp)
        assert result.data.updated_at_timestamp.seconds == "1700000000"
        assert result.meta.domain == "ampLimit"

    def test_minimal_response(self):
        data = {
            "data": {"vin": "YV1CZ000000000001"},
            "meta": {"vin": "YV1CZ000000000001", "domain": "ampLimit"},
        }
        result = parse_amp_limit_response(data)
        assert result.data.vin == "YV1CZ000000000001"
        assert result.data.amp_limit is None
        assert result.data.pending_amp_limit is None

    def test_empty_data(self):
        data = {"data": {}, "meta": {}}
        result = parse_amp_limit_response(data)
        assert result.data.vin is None


# ---------------------------------------------------------------------------
# Charge Locations - dataclass tests
# ---------------------------------------------------------------------------


class TestChargeTimer:
    def test_creation_with_values(self):
        timer = ChargeTimer(
            id="timer-1",
            activated=True,
            start="06:00",
            stop="10:00",
            active_days=["MON", "TUE", "WED"],
        )
        assert timer.id == "timer-1"
        assert timer.activated is True
        assert timer.active_days == ["MON", "TUE", "WED"]

    def test_defaults_to_none(self):
        timer = ChargeTimer()
        assert timer.id is None
        assert timer.activated is None


class TestChargeLocation:
    def test_creation_with_values(self):
        loc = ChargeLocation(
            location_id="loc-1",
            location_alias="Home",
            coordinate=ChargingCoordinate(latitude=59.3293, longitude=18.0686),
            amp_limit=16.0,
            minimum_soc=80.0,
            is_optimized_charging_enabled=True,
            is_bidirectional_charging_enabled=False,
            location_type="HOME",
        )
        assert loc.location_id == "loc-1"
        assert loc.location_alias == "Home"
        assert loc.coordinate.latitude == 59.3293
        assert loc.amp_limit == 16.0
        assert loc.minimum_soc == 80.0
        assert loc.is_optimized_charging_enabled is True
        assert loc.is_bidirectional_charging_enabled is False

    def test_defaults_to_none(self):
        loc = ChargeLocation()
        assert loc.location_id is None
        assert loc.coordinate is None
        assert loc.charge_timers is None


class TestChargeLocationsState:
    def test_creation_with_values(self):
        state = ChargeLocationsState(
            vin="YV1CZ000000000001",
            charge_locations=[ChargeLocation(location_id="loc-1")],
            utc0=True,
        )
        assert state.vin == "YV1CZ000000000001"
        assert len(state.charge_locations) == 1
        assert state.charge_locations[0].location_id == "loc-1"
        assert state.utc0 is True

    def test_defaults(self):
        state = ChargeLocationsState(vin="YV1CZ000000000001")
        assert state.charge_locations is None
        assert state.pending_charge_locations is None
        assert state.pending_delete_charge_locations is None


class TestChargeLocationsTelemetryResponse:
    def test_creation(self):
        response = ChargeLocationsTelemetryResponse(
            data=ChargeLocationsState(vin="YV1CZ000000000001"),
            meta=ChargingMeta(vin="YV1CZ000000000001", domain="chargeLocations"),
        )
        assert isinstance(response.data, ChargeLocationsState)
        assert response.meta.domain == "chargeLocations"


# ---------------------------------------------------------------------------
# Charge Locations - parser tests
# ---------------------------------------------------------------------------


class TestParseChargeLocationsResponse:
    def test_full_response(self):
        data = {
            "data": {
                "vin": "YV1CZ000000000001",
                "id": "state-1",
                "chargeLocations": [
                    {
                        "locationId": "loc-1",
                        "locationAlias": "Home",
                        "coordinate": {"latitude": 59.3293, "longitude": 18.0686},
                        "ampLimit": 16.0,
                        "minimumSoc": 80.0,
                        "isOptimizedChargingEnabled": True,
                        "isBidirectionalChargingEnabled": False,
                        "locationType": "HOME",
                        "chargeTimers": [
                            {
                                "id": "timer-1",
                                "activated": True,
                                "start": "06:00",
                                "stop": "10:00",
                                "activeDays": ["MON", "TUE"],
                            }
                        ],
                    }
                ],
                "pendingChargeLocations": [],
                "utc0": True,
                "metaReceivedAt": "2024-01-15T10:00:00Z",
                "metaEventId": "evt-456",
            },
            "meta": {"vin": "YV1CZ000000000001", "domain": "chargeLocations"},
        }
        result = parse_charge_locations_response(data)
        assert isinstance(result, ChargeLocationsTelemetryResponse)
        assert result.data.vin == "YV1CZ000000000001"
        assert len(result.data.charge_locations) == 1
        loc = result.data.charge_locations[0]
        assert loc.location_id == "loc-1"
        assert loc.location_alias == "Home"
        assert isinstance(loc.coordinate, ChargingCoordinate)
        assert loc.coordinate.latitude == 59.3293
        assert loc.amp_limit == 16.0
        assert loc.minimum_soc == 80.0
        assert loc.is_optimized_charging_enabled is True
        assert loc.is_bidirectional_charging_enabled is False
        assert loc.location_type == "HOME"
        assert len(loc.charge_timers) == 1
        assert loc.charge_timers[0].id == "timer-1"
        assert loc.charge_timers[0].activated is True
        assert result.data.utc0 is True

    def test_minimal_response(self):
        data = {
            "data": {"vin": "YV1CZ000000000001"},
            "meta": {"vin": "YV1CZ000000000001", "domain": "chargeLocations"},
        }
        result = parse_charge_locations_response(data)
        assert result.data.vin == "YV1CZ000000000001"
        assert result.data.charge_locations is None

    def test_with_pending_locations(self):
        data = {
            "data": {
                "vin": "YV1CZ000000000001",
                "pendingChargeLocations": [
                    {"locationId": "pending-1", "locationAlias": "Work"}
                ],
                "pendingDeleteChargeLocations": [
                    {"locationId": "delete-1"}
                ],
            },
            "meta": {"vin": "YV1CZ000000000001", "domain": "chargeLocations"},
        }
        result = parse_charge_locations_response(data)
        assert len(result.data.pending_charge_locations) == 1
        assert result.data.pending_charge_locations[0].location_id == "pending-1"
        assert len(result.data.pending_delete_charge_locations) == 1
        assert result.data.pending_delete_charge_locations[0].location_id == "delete-1"


# ---------------------------------------------------------------------------
# Charge Now - dataclass tests
# ---------------------------------------------------------------------------


class TestOverrideChargeTimerValue:
    def test_creation_with_values(self):
        val = OverrideChargeTimerValue(
            override=True,
            updated_at="2024-01-15T10:00:00Z",
            updated_at_timestamp=ChargingTimestamp(seconds="1700000000", nanos=0),
        )
        assert val.override is True
        assert isinstance(val.updated_at_timestamp, ChargingTimestamp)

    def test_defaults_to_none(self):
        val = OverrideChargeTimerValue()
        assert val.override is None
        assert val.updated_at is None


class TestChargeNowState:
    def test_creation_with_values(self):
        state = ChargeNowState(
            vin="YV1CZ000000000001",
            synced_override_charge_timer=OverrideChargeTimerValue(override=True),
        )
        assert state.vin == "YV1CZ000000000001"
        assert state.synced_override_charge_timer.override is True

    def test_defaults(self):
        state = ChargeNowState(vin="YV1CZ000000000001")
        assert state.synced_override_charge_timer is None
        assert state.pending_override_charge_timer is None


class TestChargeNowTelemetryResponse:
    def test_creation(self):
        response = ChargeNowTelemetryResponse(
            data=ChargeNowState(vin="YV1CZ000000000001"),
            meta=ChargingMeta(vin="YV1CZ000000000001", domain="overrideChargeTimer"),
        )
        assert isinstance(response.data, ChargeNowState)
        assert response.meta.domain == "overrideChargeTimer"


# ---------------------------------------------------------------------------
# Charge Now - parser tests
# ---------------------------------------------------------------------------


class TestParseChargeNowResponse:
    def test_full_response(self):
        data = {
            "data": {
                "vin": "YV1CZ000000000001",
                "id": "state-1",
                "syncedOverrideChargeTimer": {
                    "override": True,
                    "updatedAt": "2024-01-15T10:00:00Z",
                    "updatedAtTimestamp": {"seconds": "1700000000", "nanos": 0},
                },
                "pendingOverrideChargeTimer": {
                    "override": False,
                },
                "metaReceivedAt": "2024-01-15T10:00:00Z",
                "metaEventId": "evt-789",
            },
            "meta": {"vin": "YV1CZ000000000001", "domain": "overrideChargeTimer"},
        }
        result = parse_charge_now_response(data)
        assert isinstance(result, ChargeNowTelemetryResponse)
        assert result.data.vin == "YV1CZ000000000001"
        assert result.data.synced_override_charge_timer.override is True
        assert isinstance(result.data.synced_override_charge_timer.updated_at_timestamp, ChargingTimestamp)
        assert result.data.pending_override_charge_timer.override is False

    def test_minimal_response(self):
        data = {
            "data": {"vin": "YV1CZ000000000001"},
            "meta": {"vin": "YV1CZ000000000001", "domain": "overrideChargeTimer"},
        }
        result = parse_charge_now_response(data)
        assert result.data.vin == "YV1CZ000000000001"
        assert result.data.synced_override_charge_timer is None


# ---------------------------------------------------------------------------
# Global Charge Timer - dataclass tests
# ---------------------------------------------------------------------------


class TestGlobalChargeTimerValue:
    def test_creation_with_values(self):
        val = GlobalChargeTimerValue(
            start="06:00",
            stop="10:00",
            activated=True,
            metadata={"key": "value"},
        )
        assert val.start == "06:00"
        assert val.stop == "10:00"
        assert val.activated is True
        assert val.metadata == {"key": "value"}

    def test_defaults_to_none(self):
        val = GlobalChargeTimerValue()
        assert val.start is None
        assert val.activated is None


class TestGlobalChargeTimerState:
    def test_creation_with_values(self):
        state = GlobalChargeTimerState(
            vin="YV1CZ000000000001",
            global_charge_timer=GlobalChargeTimerValue(start="06:00", activated=True),
            utc0=False,
        )
        assert state.vin == "YV1CZ000000000001"
        assert state.global_charge_timer.start == "06:00"
        assert state.utc0 is False

    def test_defaults(self):
        state = GlobalChargeTimerState(vin="YV1CZ000000000001")
        assert state.global_charge_timer is None
        assert state.pending_global_charge_timer is None


class TestGlobalChargeTimerTelemetryResponse:
    def test_creation(self):
        response = GlobalChargeTimerTelemetryResponse(
            data=GlobalChargeTimerState(vin="YV1CZ000000000001"),
            meta=ChargingMeta(vin="YV1CZ000000000001", domain="globalChargeTimer"),
        )
        assert isinstance(response.data, GlobalChargeTimerState)
        assert response.meta.domain == "globalChargeTimer"


# ---------------------------------------------------------------------------
# Global Charge Timer - parser tests
# ---------------------------------------------------------------------------


class TestParseGlobalChargeTimerResponse:
    def test_full_response(self):
        data = {
            "data": {
                "vin": "YV1CZ000000000001",
                "id": "state-1",
                "globalChargeTimer": {
                    "start": "06:00",
                    "stop": "10:00",
                    "activated": True,
                    "metadata": {"source": "app"},
                },
                "pendingGlobalChargeTimer": {
                    "start": "07:00",
                    "stop": "11:00",
                    "activated": False,
                },
                "utc0": True,
                "metaReceivedAt": "2024-01-15T10:00:00Z",
                "metaEventId": "evt-gct-1",
            },
            "meta": {"vin": "YV1CZ000000000001", "domain": "globalChargeTimer"},
        }
        result = parse_global_charge_timer_response(data)
        assert isinstance(result, GlobalChargeTimerTelemetryResponse)
        assert result.data.vin == "YV1CZ000000000001"
        assert result.data.global_charge_timer.start == "06:00"
        assert result.data.global_charge_timer.stop == "10:00"
        assert result.data.global_charge_timer.activated is True
        assert result.data.global_charge_timer.metadata == {"source": "app"}
        assert result.data.pending_global_charge_timer.start == "07:00"
        assert result.data.pending_global_charge_timer.activated is False
        assert result.data.utc0 is True

    def test_minimal_response(self):
        data = {
            "data": {"vin": "YV1CZ000000000001"},
            "meta": {"vin": "YV1CZ000000000001", "domain": "globalChargeTimer"},
        }
        result = parse_global_charge_timer_response(data)
        assert result.data.vin == "YV1CZ000000000001"
        assert result.data.global_charge_timer is None


# ---------------------------------------------------------------------------
# Is At Charge Location - dataclass tests
# ---------------------------------------------------------------------------


class TestIsAtChargeLocationState:
    def test_creation_with_values(self):
        state = IsAtChargeLocationState(
            vin="YV1CZ000000000001",
            id="state-1",
            location_id="loc-1",
            arrived_at="2024-01-15T10:00:00Z",
            arrived_at_timestamp=ChargingTimestamp(seconds="1700000000", nanos=0),
        )
        assert state.vin == "YV1CZ000000000001"
        assert state.location_id == "loc-1"
        assert state.arrived_at == "2024-01-15T10:00:00Z"
        assert isinstance(state.arrived_at_timestamp, ChargingTimestamp)

    def test_defaults(self):
        state = IsAtChargeLocationState(vin="YV1CZ000000000001")
        assert state.location_id is None
        assert state.arrived_at is None


class TestIsAtChargeLocationResponse:
    def test_creation(self):
        response = IsAtChargeLocationResponse(
            data=IsAtChargeLocationState(vin="YV1CZ000000000001"),
            meta=ChargingMeta(vin="YV1CZ000000000001", domain="isAtChargeLocation"),
        )
        assert isinstance(response.data, IsAtChargeLocationState)
        assert response.meta.domain == "isAtChargeLocation"


# ---------------------------------------------------------------------------
# Is At Charge Location - parser tests
# ---------------------------------------------------------------------------


class TestParseIsAtChargeLocationResponse:
    def test_full_response(self):
        data = {
            "data": {
                "vin": "YV1CZ000000000001",
                "id": "state-1",
                "locationId": "loc-1",
                "arrivedAt": "2024-01-15T10:00:00Z",
                "arrivedAtTimestamp": {"seconds": "1700000000", "nanos": 0},
                "metaReceivedAt": "2024-01-15T10:00:00Z",
                "metaEventId": "evt-icl-1",
            },
            "meta": {"vin": "YV1CZ000000000001", "domain": "isAtChargeLocation"},
        }
        result = parse_is_at_charge_location_response(data)
        assert isinstance(result, IsAtChargeLocationResponse)
        assert result.data.vin == "YV1CZ000000000001"
        assert result.data.location_id == "loc-1"
        assert result.data.arrived_at == "2024-01-15T10:00:00Z"
        assert isinstance(result.data.arrived_at_timestamp, ChargingTimestamp)
        assert result.data.arrived_at_timestamp.seconds == "1700000000"

    def test_minimal_response(self):
        data = {
            "data": {"vin": "YV1CZ000000000001"},
            "meta": {"vin": "YV1CZ000000000001", "domain": "isAtChargeLocation"},
        }
        result = parse_is_at_charge_location_response(data)
        assert result.data.vin == "YV1CZ000000000001"
        assert result.data.location_id is None


# ---------------------------------------------------------------------------
# Parking Climate Timer - dataclass tests
# ---------------------------------------------------------------------------


class TestTimerSettings:
    def test_creation_with_values(self):
        settings = TimerSettings(
            seat_heating_intensity="HIGH",
            steering_wheel_heating_intensity="MEDIUM",
            requested_compartment_temperature_celsius=22.0,
            is_compartment_temperature_requested=True,
            battery_preconditioning="ON",
        )
        assert settings.seat_heating_intensity == "HIGH"
        assert settings.steering_wheel_heating_intensity == "MEDIUM"
        assert settings.requested_compartment_temperature_celsius == 22.0
        assert settings.is_compartment_temperature_requested is True
        assert settings.battery_preconditioning == "ON"

    def test_defaults_to_none(self):
        settings = TimerSettings()
        assert settings.seat_heating_intensity is None
        assert settings.battery_preconditioning is None


class TestParkingClimateTimer:
    def test_creation_with_values(self):
        timer = ParkingClimateTimer(
            timer_id="pct-1",
            index=0,
            ready_at="06:30",
            activated=True,
            repeat=True,
            weekdays=["MON", "TUE", "WED", "THU", "FRI"],
            start_date="2024-01-01",
            metadata={"key": "value"},
        )
        assert timer.timer_id == "pct-1"
        assert timer.index == 0
        assert timer.ready_at == "06:30"
        assert timer.activated is True
        assert timer.repeat is True
        assert len(timer.weekdays) == 5

    def test_defaults_to_none(self):
        timer = ParkingClimateTimer()
        assert timer.timer_id is None
        assert timer.index is None
        assert timer.weekdays is None


class TestParkingClimateTimerState:
    def test_creation_with_values(self):
        state = ParkingClimateTimerState(
            vin="YV1CZ000000000001",
            parking_climate_timers=[ParkingClimateTimer(timer_id="pct-1")],
            timer_settings=TimerSettings(seat_heating_intensity="HIGH"),
            utc0=True,
        )
        assert state.vin == "YV1CZ000000000001"
        assert len(state.parking_climate_timers) == 1
        assert state.timer_settings.seat_heating_intensity == "HIGH"
        assert state.utc0 is True

    def test_defaults(self):
        state = ParkingClimateTimerState(vin="YV1CZ000000000001")
        assert state.parking_climate_timers is None
        assert state.pending_parking_climate_timers is None
        assert state.pending_delete_parking_climate_timers is None
        assert state.timer_settings is None


class TestParkingClimateTimerTelemetryResponse:
    def test_creation(self):
        response = ParkingClimateTimerTelemetryResponse(
            data=ParkingClimateTimerState(vin="YV1CZ000000000001"),
            meta=ChargingMeta(vin="YV1CZ000000000001", domain="parkingClimateTimer"),
        )
        assert isinstance(response.data, ParkingClimateTimerState)
        assert response.meta.domain == "parkingClimateTimer"


# ---------------------------------------------------------------------------
# Parking Climate Timer - parser tests
# ---------------------------------------------------------------------------


class TestParseParkingClimateTimerResponse:
    def test_full_response(self):
        data = {
            "data": {
                "vin": "YV1CZ000000000001",
                "id": "state-1",
                "updatedAt": "2024-01-15T10:00:00Z",
                "updatedAtTimestamp": {"seconds": "1700000000", "nanos": 0},
                "parkingClimateTimers": [
                    {
                        "timerId": "pct-1",
                        "index": 0,
                        "readyAt": "06:30",
                        "activated": True,
                        "repeat": True,
                        "weekdays": ["MON", "TUE", "WED"],
                        "startDate": "2024-01-01",
                    }
                ],
                "timerSettings": {
                    "seatHeatingIntensity": "HIGH",
                    "steeringWheelHeatingIntensity": "MEDIUM",
                    "requestedCompartmentTemperatureCelsius": 22.0,
                    "isCompartmentTemperatureRequested": True,
                    "batteryPreconditioning": "ON",
                },
                "utc0": True,
                "metaReceivedAt": "2024-01-15T10:00:00Z",
                "metaEventId": "evt-pct-1",
            },
            "meta": {"vin": "YV1CZ000000000001", "domain": "parkingClimateTimer"},
        }
        result = parse_parking_climate_timer_response(data)
        assert isinstance(result, ParkingClimateTimerTelemetryResponse)
        assert result.data.vin == "YV1CZ000000000001"
        assert len(result.data.parking_climate_timers) == 1
        timer = result.data.parking_climate_timers[0]
        assert timer.timer_id == "pct-1"
        assert timer.index == 0
        assert timer.ready_at == "06:30"
        assert timer.activated is True
        assert timer.repeat is True
        assert timer.weekdays == ["MON", "TUE", "WED"]
        assert result.data.timer_settings.seat_heating_intensity == "HIGH"
        assert result.data.timer_settings.steering_wheel_heating_intensity == "MEDIUM"
        assert result.data.timer_settings.requested_compartment_temperature_celsius == 22.0
        assert result.data.timer_settings.is_compartment_temperature_requested is True
        assert result.data.timer_settings.battery_preconditioning == "ON"
        assert result.data.utc0 is True
        assert isinstance(result.data.updated_at_timestamp, ChargingTimestamp)

    def test_minimal_response(self):
        data = {
            "data": {"vin": "YV1CZ000000000001"},
            "meta": {"vin": "YV1CZ000000000001", "domain": "parkingClimateTimer"},
        }
        result = parse_parking_climate_timer_response(data)
        assert result.data.vin == "YV1CZ000000000001"
        assert result.data.parking_climate_timers is None
        assert result.data.timer_settings is None

    def test_with_pending_timers(self):
        data = {
            "data": {
                "vin": "YV1CZ000000000001",
                "pendingParkingClimateTimers": [
                    {"timerId": "pending-1", "activated": False}
                ],
                "pendingDeleteParkingClimateTimers": [
                    {"timerId": "delete-1"}
                ],
                "pendingTimerSettings": {
                    "seatHeatingIntensity": "LOW",
                },
            },
            "meta": {"vin": "YV1CZ000000000001", "domain": "parkingClimateTimer"},
        }
        result = parse_parking_climate_timer_response(data)
        assert len(result.data.pending_parking_climate_timers) == 1
        assert result.data.pending_parking_climate_timers[0].timer_id == "pending-1"
        assert len(result.data.pending_delete_parking_climate_timers) == 1
        assert result.data.pending_delete_parking_climate_timers[0].timer_id == "delete-1"
        assert result.data.pending_timer_settings.seat_heating_intensity == "LOW"


# ---------------------------------------------------------------------------
# Target SoC - dataclass tests
# ---------------------------------------------------------------------------


class TestTargetSocValue:
    def test_creation_with_values(self):
        val = TargetSocValue(
            battery_charge_target_level=80.0,
            timestamp=ChargingTimestamp(seconds="1700000000", nanos=0),
            charge_target_level_setting_type="MANUAL",
            updated_at="2024-01-15T10:00:00Z",
            source="app",
            id="tsoc-1",
        )
        assert val.battery_charge_target_level == 80.0
        assert val.charge_target_level_setting_type == "MANUAL"
        assert val.source == "app"
        assert val.id == "tsoc-1"
        assert isinstance(val.timestamp, ChargingTimestamp)

    def test_defaults_to_none(self):
        val = TargetSocValue()
        assert val.battery_charge_target_level is None
        assert val.timestamp is None
        assert val.charge_target_level_setting_type is None


class TestTargetSocState:
    def test_creation_with_values(self):
        state = TargetSocState(
            vin="YV1CZ000000000001",
            target_soc=TargetSocValue(battery_charge_target_level=80.0),
            pending_target_soc=TargetSocValue(battery_charge_target_level=90.0),
        )
        assert state.vin == "YV1CZ000000000001"
        assert state.target_soc.battery_charge_target_level == 80.0
        assert state.pending_target_soc.battery_charge_target_level == 90.0

    def test_defaults(self):
        state = TargetSocState(vin="YV1CZ000000000001")
        assert state.target_soc is None
        assert state.pending_target_soc is None


class TestTargetSocTelemetryResponse:
    def test_creation(self):
        response = TargetSocTelemetryResponse(
            data=TargetSocState(vin="YV1CZ000000000001"),
            meta=ChargingMeta(vin="YV1CZ000000000001", domain="targetSoc"),
        )
        assert isinstance(response.data, TargetSocState)
        assert response.meta.domain == "targetSoc"


# ---------------------------------------------------------------------------
# Target SoC - parser tests
# ---------------------------------------------------------------------------


class TestParseTargetSocResponse:
    def test_full_response(self):
        data = {
            "data": {
                "vin": "YV1CZ000000000001",
                "id": "state-1",
                "updatedAt": "2024-01-15T10:00:00Z",
                "timestamp": {"seconds": "1700000000", "nanos": 0},
                "targetSoc": {
                    "batteryChargeTargetLevel": 80.0,
                    "timestamp": {"seconds": "1700000000", "nanos": 0},
                    "chargeTargetLevelSettingType": "MANUAL",
                    "updatedAt": "2024-01-15T10:00:00Z",
                    "source": "app",
                    "id": "tsoc-1",
                },
                "pendingTargetSoc": {
                    "batteryChargeTargetLevel": 90.0,
                    "source": "app",
                    "id": "tsoc-2",
                },
                "metaReceivedAt": "2024-01-15T10:00:00Z",
                "metaEventId": "evt-tsoc-1",
            },
            "meta": {"vin": "YV1CZ000000000001", "domain": "targetSoc"},
        }
        result = parse_target_soc_response(data)
        assert isinstance(result, TargetSocTelemetryResponse)
        assert result.data.vin == "YV1CZ000000000001"
        assert result.data.target_soc.battery_charge_target_level == 80.0
        assert result.data.target_soc.charge_target_level_setting_type == "MANUAL"
        assert result.data.target_soc.source == "app"
        assert result.data.target_soc.id == "tsoc-1"
        assert isinstance(result.data.target_soc.timestamp, ChargingTimestamp)
        assert result.data.pending_target_soc.battery_charge_target_level == 90.0
        assert isinstance(result.data.timestamp, ChargingTimestamp)

    def test_minimal_response(self):
        data = {
            "data": {"vin": "YV1CZ000000000001"},
            "meta": {"vin": "YV1CZ000000000001", "domain": "targetSoc"},
        }
        result = parse_target_soc_response(data)
        assert result.data.vin == "YV1CZ000000000001"
        assert result.data.target_soc is None
        assert result.data.pending_target_soc is None
