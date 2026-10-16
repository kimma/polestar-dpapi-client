"""Charging settings models for Polestar API responses."""

from dataclasses import dataclass
from typing import Optional


# ---------------------------------------------------------------------------
# Shared types
# ---------------------------------------------------------------------------


@dataclass
class ChargingMeta:
    """Metadata for a charging settings response.

    Attributes:
        vin: The vehicle identification number.
        domain: The charging domain (e.g. "ampLimit", "chargeLocations").
    """

    vin: str
    domain: str


@dataclass
class ChargingTimestamp:
    """Timestamp used in charging responses.

    Attributes:
        seconds: Whole seconds since the Unix epoch.
        nanos: Nanosecond part of the timestamp.
    """

    seconds: Optional[str] = None
    nanos: Optional[int] = None


@dataclass
class ChargingCoordinate:
    """Geographic coordinate used in charge location responses.

    Attributes:
        latitude: Latitude in degrees.
        longitude: Longitude in degrees.
    """

    latitude: Optional[float] = None
    longitude: Optional[float] = None


# ---------------------------------------------------------------------------
# Amp Limit
# ---------------------------------------------------------------------------


@dataclass
class AmpLimitValue:
    """Amp limit configuration value.

    Attributes:
        amp_limit: The configured amp limit.
        updated_at: When the amp limit was last updated.
        updated_at_timestamp: Timestamp of the last update.
        source: Source of the amp limit configuration.
        id: Identifier for this amp limit value.
    """

    amp_limit: Optional[float] = None
    updated_at: Optional[str] = None
    updated_at_timestamp: Optional[ChargingTimestamp] = None
    source: Optional[str] = None
    id: Optional[str] = None


@dataclass
class AmpLimitState:
    """Vehicle amp limit state.

    Attributes:
        vin: Vehicle identification number.
        id: Identifier for this state.
        updated_at: When the state was last updated.
        updated_at_timestamp: Timestamp of the last update.
        amp_limit: Current amp limit configuration.
        pending_amp_limit: Amp limit sent to the vehicle but not yet confirmed.
        meta_received_at: When the backend received this event.
        meta_event_id: Source event identifier for this update.
    """

    vin: str
    id: Optional[str] = None
    updated_at: Optional[str] = None
    updated_at_timestamp: Optional[ChargingTimestamp] = None
    amp_limit: Optional[AmpLimitValue] = None
    pending_amp_limit: Optional[AmpLimitValue] = None
    meta_received_at: Optional[str] = None
    meta_event_id: Optional[str] = None


@dataclass
class AmpLimitTelemetryResponse:
    """Response from GET /v1/vehicles/{vin}/charging/amp-limit.

    Attributes:
        data: The amp limit state payload.
        meta: Response metadata.
    """

    data: AmpLimitState
    meta: ChargingMeta


# ---------------------------------------------------------------------------
# Charge Locations
# ---------------------------------------------------------------------------


@dataclass
class ChargeTimer:
    """Charge timer configuration within a charge location.

    Attributes:
        id: Timer identifier.
        activated: Whether the timer is activated.
        start: Start time of the timer.
        stop: Stop time of the timer.
        active_days: List of days the timer is active.
    """

    id: Optional[str] = None
    activated: Optional[bool] = None
    start: Optional[str] = None
    stop: Optional[str] = None
    active_days: Optional[list] = None


@dataclass
class ChargeLocation:
    """A configured charge location.

    Attributes:
        metadata: Metadata for this location.
        location_id: Unique identifier for the location.
        location_alias: Human-readable alias for the location.
        coordinate: Geographic coordinate of the location.
        amp_limit: Amp limit configured for this location.
        minimum_soc: Minimum state of charge for this location.
        is_optimized_charging_enabled: Whether optimized charging is enabled.
        is_bidirectional_charging_enabled: Whether bidirectional charging is enabled.
        available_optimized_charging: Available optimized charging mode.
        charge_timers: List of charge timers for this location.
        departure_times: List of configured departure times.
        location_type: Type of the charge location.
    """

    metadata: Optional[dict] = None
    location_id: Optional[str] = None
    location_alias: Optional[str] = None
    coordinate: Optional[ChargingCoordinate] = None
    amp_limit: Optional[float] = None
    minimum_soc: Optional[float] = None
    is_optimized_charging_enabled: Optional[bool] = None
    is_bidirectional_charging_enabled: Optional[bool] = None
    available_optimized_charging: Optional[str] = None
    charge_timers: Optional[list] = None
    departure_times: Optional[list] = None
    location_type: Optional[str] = None


@dataclass
class ChargeLocationsState:
    """Vehicle charge locations state.

    Attributes:
        vin: Vehicle identification number.
        id: Identifier for this state.
        charge_locations: List of configured charge locations.
        pending_charge_locations: Locations sent to the vehicle but not confirmed.
        pending_delete_charge_locations: Locations awaiting deletion on the vehicle.
        utc0: True when the vehicle reports timer times in UTC rather than local time.
        meta_received_at: When the backend received this event.
        meta_event_id: Source event identifier for this update.
    """

    vin: str
    id: Optional[str] = None
    charge_locations: Optional[list] = None
    pending_charge_locations: Optional[list] = None
    pending_delete_charge_locations: Optional[list] = None
    utc0: Optional[bool] = None
    meta_received_at: Optional[str] = None
    meta_event_id: Optional[str] = None


@dataclass
class ChargeLocationsTelemetryResponse:
    """Response from GET /v1/vehicles/{vin}/charging/charge-locations.

    Attributes:
        data: The charge locations state payload.
        meta: Response metadata.
    """

    data: ChargeLocationsState
    meta: ChargingMeta


# ---------------------------------------------------------------------------
# Charge Now (Override Charge Timer)
# ---------------------------------------------------------------------------


@dataclass
class OverrideChargeTimerValue:
    """Override charge timer value (Charge Now status).

    Attributes:
        override: True while the charge timer is overridden (Charge Now is on).
        updated_at: When the override was last updated.
        updated_at_timestamp: Timestamp of the last update.
    """

    override: Optional[bool] = None
    updated_at: Optional[str] = None
    updated_at_timestamp: Optional[ChargingTimestamp] = None


@dataclass
class ChargeNowState:
    """Vehicle charge now state.

    Attributes:
        vin: Vehicle identification number.
        id: Identifier for this state.
        synced_override_charge_timer: Override charge timer synced with the vehicle.
        pending_override_charge_timer: Override charge timer sent but not confirmed.
        meta_received_at: When the backend received this event.
        meta_event_id: Source event identifier for this update.
    """

    vin: str
    id: Optional[str] = None
    synced_override_charge_timer: Optional[OverrideChargeTimerValue] = None
    pending_override_charge_timer: Optional[OverrideChargeTimerValue] = None
    meta_received_at: Optional[str] = None
    meta_event_id: Optional[str] = None


@dataclass
class ChargeNowTelemetryResponse:
    """Response from GET /v1/vehicles/{vin}/charging/charge-now.

    Attributes:
        data: The charge now state payload.
        meta: Response metadata.
    """

    data: ChargeNowState
    meta: ChargingMeta


# ---------------------------------------------------------------------------
# Global Charge Timer
# ---------------------------------------------------------------------------


@dataclass
class GlobalChargeTimerValue:
    """Global charge timer configuration value.

    Attributes:
        start: Start time of the global charge timer.
        stop: Stop time of the global charge timer.
        activated: Whether the global charge timer is activated.
        metadata: Metadata for this timer.
    """

    start: Optional[str] = None
    stop: Optional[str] = None
    activated: Optional[bool] = None
    metadata: Optional[dict] = None


@dataclass
class GlobalChargeTimerState:
    """Vehicle global charge timer state.

    Attributes:
        vin: Vehicle identification number.
        id: Identifier for this state.
        global_charge_timer: Current global charge timer configuration.
        pending_global_charge_timer: Timer sent to the vehicle but not confirmed.
        utc0: True when the vehicle reports timer times in UTC rather than local time.
        meta_received_at: When the backend received this event.
        meta_event_id: Source event identifier for this update.
    """

    vin: str
    id: Optional[str] = None
    global_charge_timer: Optional[GlobalChargeTimerValue] = None
    pending_global_charge_timer: Optional[GlobalChargeTimerValue] = None
    utc0: Optional[bool] = None
    meta_received_at: Optional[str] = None
    meta_event_id: Optional[str] = None


@dataclass
class GlobalChargeTimerTelemetryResponse:
    """Response from GET /v1/vehicles/{vin}/charging/global-charge-timer.

    Attributes:
        data: The global charge timer state payload.
        meta: Response metadata.
    """

    data: GlobalChargeTimerState
    meta: ChargingMeta


# ---------------------------------------------------------------------------
# Is At Charge Location
# ---------------------------------------------------------------------------


@dataclass
class IsAtChargeLocationState:
    """State indicating whether the vehicle is at a charge location.

    Attributes:
        vin: Vehicle identification number.
        id: Identifier for this state.
        location_id: The charge location the vehicle is currently at.
        arrived_at: When the vehicle arrived at the location.
        arrived_at_timestamp: Timestamp of arrival.
        meta_received_at: When the backend received this event.
        meta_event_id: Source event identifier for this update.
    """

    vin: str
    id: Optional[str] = None
    location_id: Optional[str] = None
    arrived_at: Optional[str] = None
    arrived_at_timestamp: Optional[ChargingTimestamp] = None
    meta_received_at: Optional[str] = None
    meta_event_id: Optional[str] = None


@dataclass
class IsAtChargeLocationResponse:
    """Response from GET /v1/vehicles/{vin}/charging/is-at-charge-location.

    Attributes:
        data: The is-at-charge-location state payload.
        meta: Response metadata.
    """

    data: IsAtChargeLocationState
    meta: ChargingMeta


# ---------------------------------------------------------------------------
# Parking Climate Timer
# ---------------------------------------------------------------------------


@dataclass
class TimerSettings:
    """Settings for a parking climate timer.

    Attributes:
        seat_heating_intensity: Intensity of seat heating.
        steering_wheel_heating_intensity: Intensity of steering wheel heating.
        requested_compartment_temperature_celsius: Requested cabin temperature.
        is_compartment_temperature_requested: Whether cabin temperature is requested.
        battery_preconditioning: Battery preconditioning setting.
    """

    seat_heating_intensity: Optional[str] = None
    steering_wheel_heating_intensity: Optional[str] = None
    requested_compartment_temperature_celsius: Optional[float] = None
    is_compartment_temperature_requested: Optional[bool] = None
    battery_preconditioning: Optional[str] = None


@dataclass
class ParkingClimateTimer:
    """A parking climate timer configuration.

    Attributes:
        timer_id: Unique identifier for the timer.
        index: Index position of the timer.
        ready_at: Time the vehicle should be ready.
        activated: Whether the timer is activated.
        repeat: True when the timer repeats weekly on the listed weekdays.
        weekdays: List of weekdays the timer is active.
        start_date: Start date for the timer.
        metadata: Metadata for this timer.
    """

    timer_id: Optional[str] = None
    index: Optional[int] = None
    ready_at: Optional[str] = None
    activated: Optional[bool] = None
    repeat: Optional[bool] = None
    weekdays: Optional[list] = None
    start_date: Optional[str] = None
    metadata: Optional[dict] = None


@dataclass
class ParkingClimateTimerState:
    """Vehicle parking climate timer state.

    Attributes:
        vin: Vehicle identification number.
        id: Identifier for this state.
        updated_at: When the state was last updated.
        updated_at_timestamp: Timestamp of the last update.
        parking_climate_timers: List of parking climate timers.
        pending_parking_climate_timers: Timers sent but not confirmed.
        pending_delete_parking_climate_timers: Timers awaiting deletion.
        timer_settings: Current timer settings.
        pending_timer_settings: Timer settings sent but not confirmed.
        utc0: True when the vehicle reports timer times in UTC rather than local time.
        meta_received_at: When the backend received this event.
        meta_event_id: Source event identifier for this update.
    """

    vin: str
    id: Optional[str] = None
    updated_at: Optional[str] = None
    updated_at_timestamp: Optional[ChargingTimestamp] = None
    parking_climate_timers: Optional[list] = None
    pending_parking_climate_timers: Optional[list] = None
    pending_delete_parking_climate_timers: Optional[list] = None
    timer_settings: Optional[TimerSettings] = None
    pending_timer_settings: Optional[TimerSettings] = None
    utc0: Optional[bool] = None
    meta_received_at: Optional[str] = None
    meta_event_id: Optional[str] = None


@dataclass
class ParkingClimateTimerTelemetryResponse:
    """Response from GET /v1/vehicles/{vin}/charging/parking-climate-timer.

    Attributes:
        data: The parking climate timer state payload.
        meta: Response metadata.
    """

    data: ParkingClimateTimerState
    meta: ChargingMeta


# ---------------------------------------------------------------------------
# Target SoC
# ---------------------------------------------------------------------------


@dataclass
class TargetSocValue:
    """Target state of charge configuration value.

    Attributes:
        battery_charge_target_level: Target battery charge level percentage.
        timestamp: Timestamp of the target SoC configuration.
        charge_target_level_setting_type: Type of the charge target level setting.
        updated_at: When the target SoC was last updated.
        source: Source of the target SoC configuration.
        id: Identifier for this target SoC value.
    """

    battery_charge_target_level: Optional[float] = None
    timestamp: Optional[ChargingTimestamp] = None
    charge_target_level_setting_type: Optional[str] = None
    updated_at: Optional[str] = None
    source: Optional[str] = None
    id: Optional[str] = None


@dataclass
class TargetSocState:
    """Vehicle target state of charge state.

    Attributes:
        vin: Vehicle identification number.
        id: Identifier for this state.
        updated_at: When the state was last updated.
        timestamp: Timestamp of the state.
        target_soc: Current target SoC configuration.
        pending_target_soc: Target SoC sent to the vehicle but not confirmed.
        meta_received_at: When the backend received this event.
        meta_event_id: Source event identifier for this update.
    """

    vin: str
    id: Optional[str] = None
    updated_at: Optional[str] = None
    timestamp: Optional[ChargingTimestamp] = None
    target_soc: Optional[TargetSocValue] = None
    pending_target_soc: Optional[TargetSocValue] = None
    meta_received_at: Optional[str] = None
    meta_event_id: Optional[str] = None


@dataclass
class TargetSocTelemetryResponse:
    """Response from GET /v1/vehicles/{vin}/charging/target-soc.

    Attributes:
        data: The target SoC state payload.
        meta: Response metadata.
    """

    data: TargetSocState
    meta: ChargingMeta
