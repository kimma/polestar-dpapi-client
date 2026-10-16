"""Telemetry-related models for Polestar API responses."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class TelemetryTimestamp:
    """Timestamp used in telemetry state responses.

    Attributes:
        seconds: Whole seconds since the Unix epoch.
        nanos: Nanosecond part of the timestamp.
    """

    seconds: str
    nanos: int


@dataclass
class TelemetryCoordinate:
    """Geographic coordinate used in location telemetry.

    Attributes:
        latitude: Latitude in degrees.
        longitude: Longitude in degrees.
    """

    latitude: float
    longitude: float


@dataclass
class TelemetryMeta:
    """Metadata for a telemetry response.

    Attributes:
        vin: The vehicle identification number.
        domain: The telemetry domain (e.g. "availability", "battery").
    """

    vin: str
    domain: str


# ---------------------------------------------------------------------------
# Availability
# ---------------------------------------------------------------------------


@dataclass
class AvailabilityState:
    """Vehicle availability state.

    Attributes:
        vin: Vehicle identification number.
        timestamp: When the telemetry was recorded on the vehicle.
        availability_status: Reported vehicle availability status.
        unavailable_reason: Reason returned when the vehicle is not available.
        usage_mode: Current usage mode reported for the vehicle.
        meta_received_at: When the backend received this telemetry event.
        meta_event_id: Source event identifier for this telemetry update.
    """

    vin: str
    timestamp: Optional[TelemetryTimestamp] = None
    availability_status: Optional[str] = None
    unavailable_reason: Optional[str] = None
    usage_mode: Optional[str] = None
    meta_received_at: Optional[str] = None
    meta_event_id: Optional[str] = None


@dataclass
class AvailabilityTelemetryResponse:
    """Response from GET /v1/vehicles/{vin}/telemetry/availability.

    Attributes:
        data: The availability state payload.
        meta: Response metadata.
    """

    data: AvailabilityState
    meta: TelemetryMeta


# ---------------------------------------------------------------------------
# Battery
# ---------------------------------------------------------------------------


@dataclass
class EnergyConsumptionPercentage:
    """Breakdown of energy consumption as percentages.

    Attributes:
        other: Percentage attributed to other systems.
        driving: Percentage attributed to driving.
        climate: Percentage attributed to climate control.
        battery: Percentage attributed to battery conditioning.
    """

    other: Optional[float] = None
    driving: Optional[float] = None
    climate: Optional[float] = None
    battery: Optional[float] = None


@dataclass
class EnergyConsumptionWh:
    """Breakdown of energy consumption in watt-hours.

    Attributes:
        other: Watt-hours attributed to other systems.
        driving: Watt-hours attributed to driving.
        climate: Watt-hours attributed to climate control.
        battery: Watt-hours attributed to battery conditioning.
    """

    other: Optional[float] = None
    driving: Optional[float] = None
    climate: Optional[float] = None
    battery: Optional[float] = None


@dataclass
class DischargeInfo:
    """Vehicle-to-grid / vehicle-to-load discharge information.

    Attributes:
        energy_available: Available discharge energy.
        energy_available_increase: Increase in available energy.
        power_limit: Discharge power limit.
    """

    energy_available: Optional[float] = None
    energy_available_increase: Optional[float] = None
    power_limit: Optional[float] = None


@dataclass
class ManualPreconditioning:
    """Manual preconditioning state.

    Attributes:
        preconditioning_status: Current preconditioning status.
        unavailable_reason: Reason preconditioning is unavailable.
        started_at: When preconditioning started.
        ending_at: When preconditioning is expected to end.
    """

    preconditioning_status: Optional[str] = None
    unavailable_reason: Optional[str] = None
    started_at: Optional[TelemetryTimestamp] = None
    ending_at: Optional[TelemetryTimestamp] = None


@dataclass
class BatteryState:
    """Vehicle battery state.

    Attributes:
        vin: Vehicle identification number.
        timestamp: When the telemetry was recorded on the vehicle.
        average_energy_consumption_kwh_per_100_km: Average energy consumption.
        average_energy_consumption_kwh_per_100_km_automatic: Automatic mode consumption.
        average_energy_consumption_kwh_per_100_km_since_charge: Consumption since charge.
        battery_charge_level_percentage: Current battery charge level.
        charger_connection_status: Charger connection status.
        charger_power_status: Charger power status.
        charging_current_amps: Charging current in amps.
        charging_power_watts: Charging power in watts.
        charging_status: Charging status (deprecated, prefer charging_status_v2).
        charging_status_v2: Extended charging status.
        charging_type: Type of charging (AC, DC, wireless).
        charging_voltage_volts: Charging voltage.
        discharge_info: Discharge information for V2G/V2L.
        energy_consumption_percentage_manual: Manual mode energy breakdown (%).
        energy_consumption_percentage_automatic: Automatic mode energy breakdown (%).
        energy_consumption_percentage_since_charge: Since-charge energy breakdown (%).
        energy_consumption_wh_manual: Manual mode energy breakdown (Wh).
        energy_consumption_wh_automatic: Automatic mode energy breakdown (Wh).
        energy_consumption_wh_since_charge: Since-charge energy breakdown (Wh).
        estimated_charging_time_to_full_minutes: Estimated time to full charge.
        estimated_charging_time_minutes_to_target_distance: Time to target distance.
        estimated_charging_time_minutes_to_minimum_soc: Time to minimum SoC.
        estimated_distance_to_empty_km: Estimated range in km.
        estimated_distance_to_empty_miles: Estimated range in miles.
        manual_preconditioning: Manual preconditioning state.
        total_energy_consumption_wh: Total energy consumption in Wh.
        total_energy_consumption_wh_automatic: Total automatic consumption in Wh.
        total_energy_consumption_wh_since_charge: Total since-charge consumption in Wh.
        meta_received_at: When the backend received this telemetry event.
        meta_event_id: Source event identifier for this telemetry update.
    """

    vin: str
    timestamp: Optional[TelemetryTimestamp] = None
    average_energy_consumption_kwh_per_100_km: Optional[float] = None
    average_energy_consumption_kwh_per_100_km_automatic: Optional[float] = None
    average_energy_consumption_kwh_per_100_km_since_charge: Optional[float] = None
    battery_charge_level_percentage: Optional[float] = None
    charger_connection_status: Optional[str] = None
    charger_power_status: Optional[str] = None
    charging_current_amps: Optional[float] = None
    charging_power_watts: Optional[float] = None
    charging_status: Optional[str] = None
    charging_status_v2: Optional[str] = None
    charging_type: Optional[str] = None
    charging_voltage_volts: Optional[float] = None
    discharge_info: Optional[DischargeInfo] = None
    energy_consumption_percentage_manual: Optional[EnergyConsumptionPercentage] = None
    energy_consumption_percentage_automatic: Optional[EnergyConsumptionPercentage] = None
    energy_consumption_percentage_since_charge: Optional[EnergyConsumptionPercentage] = None
    energy_consumption_wh_manual: Optional[EnergyConsumptionWh] = None
    energy_consumption_wh_automatic: Optional[EnergyConsumptionWh] = None
    energy_consumption_wh_since_charge: Optional[EnergyConsumptionWh] = None
    estimated_charging_time_to_full_minutes: Optional[int] = None
    estimated_charging_time_minutes_to_target_distance: Optional[int] = None
    estimated_charging_time_minutes_to_minimum_soc: Optional[int] = None
    estimated_distance_to_empty_km: Optional[float] = None
    estimated_distance_to_empty_miles: Optional[float] = None
    manual_preconditioning: Optional[ManualPreconditioning] = None
    total_energy_consumption_wh: Optional[float] = None
    total_energy_consumption_wh_automatic: Optional[float] = None
    total_energy_consumption_wh_since_charge: Optional[float] = None
    meta_received_at: Optional[str] = None
    meta_event_id: Optional[str] = None


@dataclass
class BatteryTelemetryResponse:
    """Response from GET /v1/vehicles/{vin}/telemetry/battery.

    Attributes:
        data: The battery state payload.
        meta: Response metadata.
    """

    data: BatteryState
    meta: TelemetryMeta


# ---------------------------------------------------------------------------
# Exterior
# ---------------------------------------------------------------------------


@dataclass
class ExteriorState:
    """Vehicle exterior state (doors, locks, windows, hood, trunk).

    Attributes:
        vin: Vehicle identification number.
        timestamp: When the telemetry was recorded on the vehicle.
        central_lock: Central lock status.
        front_left_door: Front-left door status.
        front_right_door: Front-right door status.
        rear_left_door: Rear-left door status.
        rear_right_door: Rear-right door status.
        front_left_window: Front-left window status.
        front_right_window: Front-right window status.
        rear_left_window: Rear-left window status.
        rear_right_window: Rear-right window status.
        hood: Hood status.
        fuel_flap: Fuel flap / charge port status.
        trunk: Trunk status.
        sunroof: Sunroof status.
        alarm: Alarm status.
        tailgate_lock: Tailgate lock status.
        meta_received_at: When the backend received this telemetry event.
        meta_event_id: Source event identifier for this telemetry update.
    """

    vin: str
    timestamp: Optional[TelemetryTimestamp] = None
    central_lock: Optional[str] = None
    front_left_door: Optional[str] = None
    front_right_door: Optional[str] = None
    rear_left_door: Optional[str] = None
    rear_right_door: Optional[str] = None
    front_left_window: Optional[str] = None
    front_right_window: Optional[str] = None
    rear_left_window: Optional[str] = None
    rear_right_window: Optional[str] = None
    hood: Optional[str] = None
    fuel_flap: Optional[str] = None
    trunk: Optional[str] = None
    sunroof: Optional[str] = None
    alarm: Optional[str] = None
    tailgate_lock: Optional[str] = None
    meta_received_at: Optional[str] = None
    meta_event_id: Optional[str] = None


@dataclass
class ExteriorTelemetryResponse:
    """Response from GET /v1/vehicles/{vin}/telemetry/exterior.

    Attributes:
        data: The exterior state payload.
        meta: Response metadata.
    """

    data: ExteriorState
    meta: TelemetryMeta


# ---------------------------------------------------------------------------
# Health
# ---------------------------------------------------------------------------


@dataclass
class LightWarnings:
    """Exterior light warning indicators.

    Each field is one of: UNSPECIFIED, NO_WARNING, FAILURE.
    """

    turn_indicator_front_left: Optional[str] = None
    turn_indicator_front_right: Optional[str] = None
    turn_indicator_rear_left: Optional[str] = None
    turn_indicator_rear_right: Optional[str] = None
    turn_indicator_left: Optional[str] = None
    turn_indicator_right: Optional[str] = None
    turn_indicator_side_left: Optional[str] = None
    turn_indicator_side_right: Optional[str] = None
    low_beam_left: Optional[str] = None
    low_beam_right: Optional[str] = None
    low_beam_any: Optional[str] = None
    high_beam_left: Optional[str] = None
    high_beam_right: Optional[str] = None
    high_beam_any: Optional[str] = None
    fog_light_front: Optional[str] = None
    fog_light_rear: Optional[str] = None
    fog_light_rear_left: Optional[str] = None
    fog_light_rear_right: Optional[str] = None
    brake_light_left: Optional[str] = None
    brake_light_right: Optional[str] = None
    brake_light_center: Optional[str] = None
    brake_light_any: Optional[str] = None
    position_light_front_left: Optional[str] = None
    position_light_front_right: Optional[str] = None
    position_light_rear_left: Optional[str] = None
    position_light_rear_right: Optional[str] = None
    position_light_front: Optional[str] = None
    position_light_rear: Optional[str] = None
    daytime_running_light_left: Optional[str] = None
    daytime_running_light_right: Optional[str] = None
    daytime_running_light_any: Optional[str] = None
    registration_plate_light: Optional[str] = None
    side_marker_light_left: Optional[str] = None
    side_marker_light_right: Optional[str] = None
    side_marker_light_any: Optional[str] = None
    reverse_light_left: Optional[str] = None
    reverse_light_right: Optional[str] = None
    reverse_light_any: Optional[str] = None
    cornering_light_left: Optional[str] = None
    cornering_light_right: Optional[str] = None


@dataclass
class HealthState:
    """Vehicle health state (service warnings, tyre pressures, fluid levels).

    Attributes:
        vin: Vehicle identification number.
        timestamp: When the telemetry was recorded on the vehicle.
        engine_hours_to_service: Engine hours remaining until service.
        days_to_service: Days remaining until service.
        distance_to_service_km: Distance remaining until service.
        service_warning: Current service warning state.
        brake_fluid_level_warning: Brake fluid warning.
        engine_coolant_level_warning: Engine coolant warning.
        oil_level_warning: Oil level warning.
        washer_fluid_level_warning: Washer fluid warning.
        front_left_tyre_pressure_warning: Front-left tyre pressure warning.
        front_right_tyre_pressure_warning: Front-right tyre pressure warning.
        rear_left_tyre_pressure_warning: Rear-left tyre pressure warning.
        rear_right_tyre_pressure_warning: Rear-right tyre pressure warning.
        front_left_tyre_pressure_kpa: Front-left tyre pressure in kPa.
        front_right_tyre_pressure_kpa: Front-right tyre pressure in kPa.
        rear_left_tyre_pressure_kpa: Rear-left tyre pressure in kPa.
        rear_right_tyre_pressure_kpa: Rear-right tyre pressure in kPa.
        front_tyres_reference_pressure_kpa: Recommended front tyre pressure.
        rear_tyres_reference_pressure_kpa: Recommended rear tyre pressure.
        low_voltage_battery_warning: Low-voltage battery warning status.
        light_warnings: Exterior light warning indicators.
        meta_received_at: When the backend received this telemetry event.
        meta_event_id: Source event identifier for this telemetry update.
    """

    vin: str
    timestamp: Optional[TelemetryTimestamp] = None
    engine_hours_to_service: Optional[float] = None
    days_to_service: Optional[float] = None
    distance_to_service_km: Optional[float] = None
    service_warning: Optional[str] = None
    brake_fluid_level_warning: Optional[str] = None
    engine_coolant_level_warning: Optional[str] = None
    oil_level_warning: Optional[str] = None
    washer_fluid_level_warning: Optional[str] = None
    front_left_tyre_pressure_warning: Optional[str] = None
    front_right_tyre_pressure_warning: Optional[str] = None
    rear_left_tyre_pressure_warning: Optional[str] = None
    rear_right_tyre_pressure_warning: Optional[str] = None
    front_left_tyre_pressure_kpa: Optional[float] = None
    front_right_tyre_pressure_kpa: Optional[float] = None
    rear_left_tyre_pressure_kpa: Optional[float] = None
    rear_right_tyre_pressure_kpa: Optional[float] = None
    front_tyres_reference_pressure_kpa: Optional[float] = None
    rear_tyres_reference_pressure_kpa: Optional[float] = None
    low_voltage_battery_warning: Optional[str] = None
    light_warnings: Optional[LightWarnings] = None
    meta_received_at: Optional[str] = None
    meta_event_id: Optional[str] = None


@dataclass
class HealthTelemetryResponse:
    """Response from GET /v1/vehicles/{vin}/telemetry/health.

    Attributes:
        data: The health state payload.
        meta: Response metadata.
    """

    data: HealthState
    meta: TelemetryMeta


# ---------------------------------------------------------------------------
# Location
# ---------------------------------------------------------------------------


@dataclass
class LocationState:
    """Vehicle location state.

    Attributes:
        vin: Vehicle identification number.
        timestamp: When the telemetry was recorded on the vehicle.
        altitude: Altitude in metres (reported as string by API).
        coordinate: Geographic coordinate.
        heading: Heading in degrees from true north.
        speed: Speed in km/h (reported as string by API).
        meta_received_at: When the backend received this telemetry event.
        meta_event_id: Source event identifier for this telemetry update.
    """

    vin: str
    timestamp: Optional[TelemetryTimestamp] = None
    altitude: Optional[str] = None
    coordinate: Optional[TelemetryCoordinate] = None
    heading: Optional[float] = None
    speed: Optional[str] = None
    meta_received_at: Optional[str] = None
    meta_event_id: Optional[str] = None


@dataclass
class LocationTelemetryResponse:
    """Response from GET /v1/vehicles/{vin}/telemetry/location.

    Attributes:
        data: The location state payload.
        meta: Response metadata.
    """

    data: LocationState
    meta: TelemetryMeta


# ---------------------------------------------------------------------------
# Odometer
# ---------------------------------------------------------------------------


@dataclass
class OdometerState:
    """Vehicle odometer state.

    Attributes:
        vin: Vehicle identification number.
        timestamp: When the telemetry was recorded on the vehicle.
        odometer_meters: Total odometer reading in meters.
        trip_meter_manual_km: Trip meter (manual reset) in km.
        average_speed_km_per_hour: Average speed (manual) in km/h.
        trip_meter_automatic_km: Trip meter (automatic reset) in km.
        average_speed_km_per_hour_automatic: Average speed (automatic) in km/h.
        trip_meter_since_charge_km: Trip meter since last charge in km.
        average_speed_km_per_hour_since_charge: Average speed since charge in km/h.
        meta_received_at: When the backend received this telemetry event.
        meta_event_id: Source event identifier for this telemetry update.
    """

    vin: str
    timestamp: Optional[TelemetryTimestamp] = None
    odometer_meters: Optional[float] = None
    trip_meter_manual_km: Optional[float] = None
    average_speed_km_per_hour: Optional[float] = None
    trip_meter_automatic_km: Optional[float] = None
    average_speed_km_per_hour_automatic: Optional[float] = None
    trip_meter_since_charge_km: Optional[float] = None
    average_speed_km_per_hour_since_charge: Optional[float] = None
    meta_received_at: Optional[str] = None
    meta_event_id: Optional[str] = None


@dataclass
class OdometerTelemetryResponse:
    """Response from GET /v1/vehicles/{vin}/telemetry/odometer.

    Attributes:
        data: The odometer state payload.
        meta: Response metadata.
    """

    data: OdometerState
    meta: TelemetryMeta


# ---------------------------------------------------------------------------
# Parking Climatization
# ---------------------------------------------------------------------------


@dataclass
class ParkingClimatizationState:
    """Vehicle parking climatization state.

    Attributes:
        vin: Vehicle identification number.
        timestamp: When the telemetry was recorded on the vehicle.
        running_status: Current running status.
        main_climate_running_status: Main climate running status.
        runtime_left_minutes: Remaining runtime in minutes (deprecated).
        errors: Active parking-climatization errors.
        warnings: Active parking-climatization warnings.
        ventilation: Ventilation mode.
        current_compartment_temperature_celsius: Current cabin temperature.
        requested_compartment_temperature_celsius: Requested cabin temperature.
        requested_front_left_seat: Front-left seat heating level.
        requested_front_right_seat: Front-right seat heating level.
        requested_rear_left_seat: Rear-left seat heating level.
        requested_rear_right_seat: Rear-right seat heating level.
        requested_steering_wheel_heating: Steering wheel heating level.
        started_at: When climatization started.
        ending_at: When climatization is expected to end.
        start_reason: Reason climatization started.
        meta_received_at: When the backend received this telemetry event.
        meta_event_id: Source event identifier for this telemetry update.
    """

    vin: str
    timestamp: Optional[TelemetryTimestamp] = None
    running_status: Optional[str] = None
    main_climate_running_status: Optional[str] = None
    runtime_left_minutes: Optional[int] = None
    errors: Optional[list] = None
    warnings: Optional[list] = None
    ventilation: Optional[str] = None
    current_compartment_temperature_celsius: Optional[float] = None
    requested_compartment_temperature_celsius: Optional[float] = None
    requested_front_left_seat: Optional[str] = None
    requested_front_right_seat: Optional[str] = None
    requested_rear_left_seat: Optional[str] = None
    requested_rear_right_seat: Optional[str] = None
    requested_steering_wheel_heating: Optional[str] = None
    started_at: Optional[TelemetryTimestamp] = None
    ending_at: Optional[TelemetryTimestamp] = None
    start_reason: Optional[str] = None
    meta_received_at: Optional[str] = None
    meta_event_id: Optional[str] = None


@dataclass
class ParkingClimatizationTelemetryResponse:
    """Response from GET /v1/vehicles/{vin}/telemetry/parking-climatization.

    Attributes:
        data: The parking climatization state payload.
        meta: Response metadata.
    """

    data: ParkingClimatizationState
    meta: TelemetryMeta


# ---------------------------------------------------------------------------
# Pre-Cleaning
# ---------------------------------------------------------------------------


@dataclass
class PreCleaningState:
    """Vehicle cabin pre-cleaning state.

    Attributes:
        vin: Vehicle identification number.
        timestamp: When the telemetry was recorded on the vehicle.
        last_cycle_completed: When the last cycle completed.
        measurement_date: When the air quality was measured.
        started_at: When pre-cleaning started.
        ending_at: When pre-cleaning is expected to end.
        running_status: Current running status.
        start_reason: Reason pre-cleaning started.
        last_cycle_valid: Whether the last cycle was valid.
        measured_air_quality_index: Measured air quality index.
        measured_particulate_matter_25: Measured PM2.5 value.
        runtime_left_minutes: Remaining runtime in minutes.
        error: Current error type.
        meta_received_at: When the backend received this telemetry event.
        meta_event_id: Source event identifier for this telemetry update.
    """

    vin: str
    timestamp: Optional[TelemetryTimestamp] = None
    last_cycle_completed: Optional[TelemetryTimestamp] = None
    measurement_date: Optional[TelemetryTimestamp] = None
    started_at: Optional[TelemetryTimestamp] = None
    ending_at: Optional[TelemetryTimestamp] = None
    running_status: Optional[str] = None
    start_reason: Optional[str] = None
    last_cycle_valid: Optional[bool] = None
    measured_air_quality_index: Optional[int] = None
    measured_particulate_matter_25: Optional[float] = None
    runtime_left_minutes: Optional[int] = None
    error: Optional[str] = None
    meta_received_at: Optional[str] = None
    meta_event_id: Optional[str] = None


@dataclass
class PreCleaningTelemetryResponse:
    """Response from GET /v1/vehicles/{vin}/telemetry/pre-cleaning.

    Attributes:
        data: The pre-cleaning state payload.
        meta: Response metadata.
    """

    data: PreCleaningState
    meta: TelemetryMeta
