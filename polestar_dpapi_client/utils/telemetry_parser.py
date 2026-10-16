"""Helpers for parsing Polestar telemetry API responses."""

from polestar_dpapi_client.models.telemetry import (
    TelemetryTimestamp,
    TelemetryCoordinate,
    TelemetryMeta,
    AvailabilityState,
    AvailabilityTelemetryResponse,
    EnergyConsumptionPercentage,
    EnergyConsumptionWh,
    DischargeInfo,
    ManualPreconditioning,
    BatteryState,
    BatteryTelemetryResponse,
    ExteriorState,
    ExteriorTelemetryResponse,
    LightWarnings,
    HealthState,
    HealthTelemetryResponse,
    LocationState,
    LocationTelemetryResponse,
    OdometerState,
    OdometerTelemetryResponse,
    ParkingClimatizationState,
    ParkingClimatizationTelemetryResponse,
    PreCleaningState,
    PreCleaningTelemetryResponse,
)
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


def _parse_timestamp(data: dict | None) -> TelemetryTimestamp | None:
    if data is None:
        return None
    return TelemetryTimestamp(seconds=data.get("seconds"), nanos=data.get("nanos"))


def _parse_coordinate(data: dict | None) -> TelemetryCoordinate | None:
    if data is None:
        return None
    return TelemetryCoordinate(
        latitude=data.get("latitude"),
        longitude=data.get("longitude"),
    )


def _parse_meta(data: dict) -> TelemetryMeta:
    return TelemetryMeta(vin=data.get("vin"), domain=data.get("domain"))


def _parse_energy_consumption_percentage(data: dict | None) -> EnergyConsumptionPercentage | None:
    if data is None:
        return None
    return EnergyConsumptionPercentage(
        other=data.get("other"),
        driving=data.get("driving"),
        climate=data.get("climate"),
        battery=data.get("battery"),
    )


def _parse_energy_consumption_wh(data: dict | None) -> EnergyConsumptionWh | None:
    if data is None:
        return None
    return EnergyConsumptionWh(
        other=data.get("other"),
        driving=data.get("driving"),
        climate=data.get("climate"),
        battery=data.get("battery"),
    )


def _parse_discharge_info(data: dict | None) -> DischargeInfo | None:
    if data is None:
        return None
    return DischargeInfo(
        energy_available=data.get("energyAvailable"),
        energy_available_increase=data.get("energyAvailableIncrease"),
        power_limit=data.get("powerLimit"),
    )


def _parse_manual_preconditioning(data: dict | None) -> ManualPreconditioning | None:
    if data is None:
        return None
    return ManualPreconditioning(
        preconditioning_status=data.get("preconditioningStatus"),
        unavailable_reason=data.get("unavailableReason"),
        started_at=_parse_timestamp(data.get("startedAt")),
        ending_at=_parse_timestamp(data.get("endingAt")),
    )


def _parse_light_warnings(data: dict | None) -> LightWarnings | None:
    if data is None:
        return None
    return LightWarnings(
        turn_indicator_front_left=data.get("turnIndicatorFrontLeft"),
        turn_indicator_front_right=data.get("turnIndicatorFrontRight"),
        turn_indicator_rear_left=data.get("turnIndicatorRearLeft"),
        turn_indicator_rear_right=data.get("turnIndicatorRearRight"),
        turn_indicator_left=data.get("turnIndicatorLeft"),
        turn_indicator_right=data.get("turnIndicatorRight"),
        turn_indicator_side_left=data.get("turnIndicatorSideLeft"),
        turn_indicator_side_right=data.get("turnIndicatorSideRight"),
        low_beam_left=data.get("lowBeamLeft"),
        low_beam_right=data.get("lowBeamRight"),
        low_beam_any=data.get("lowBeamAny"),
        high_beam_left=data.get("highBeamLeft"),
        high_beam_right=data.get("highBeamRight"),
        high_beam_any=data.get("highBeamAny"),
        fog_light_front=data.get("fogLightFront"),
        fog_light_rear=data.get("fogLightRear"),
        fog_light_rear_left=data.get("fogLightRearLeft"),
        fog_light_rear_right=data.get("fogLightRearRight"),
        brake_light_left=data.get("brakeLightLeft"),
        brake_light_right=data.get("brakeLightRight"),
        brake_light_center=data.get("brakeLightCenter"),
        brake_light_any=data.get("brakeLightAny"),
        position_light_front_left=data.get("positionLightFrontLeft"),
        position_light_front_right=data.get("positionLightFrontRight"),
        position_light_rear_left=data.get("positionLightRearLeft"),
        position_light_rear_right=data.get("positionLightRearRight"),
        position_light_front=data.get("positionLightFront"),
        position_light_rear=data.get("positionLightRear"),
        daytime_running_light_left=data.get("daytimeRunningLightLeft"),
        daytime_running_light_right=data.get("daytimeRunningLightRight"),
        daytime_running_light_any=data.get("daytimeRunningLightAny"),
        registration_plate_light=data.get("registrationPlateLight"),
        side_marker_light_left=data.get("sideMarkerLightLeft"),
        side_marker_light_right=data.get("sideMarkerLightRight"),
        side_marker_light_any=data.get("sideMarkerLightAny"),
        reverse_light_left=data.get("reverseLightLeft"),
        reverse_light_right=data.get("reverseLightRight"),
        reverse_light_any=data.get("reverseLightAny"),
        cornering_light_left=data.get("corneringLightLeft"),
        cornering_light_right=data.get("corneringLightRight"),
    )


# ---------------------------------------------------------------------------
# Top-level parsers
# ---------------------------------------------------------------------------


def parse_availability_response(data: dict) -> AvailabilityTelemetryResponse:
    """Parse JSON response for availability telemetry endpoint."""
    state_data = data.get("data", {})
    return AvailabilityTelemetryResponse(
        data=AvailabilityState(
            vin=state_data.get("vin"),
            timestamp=_parse_timestamp(state_data.get("timestamp")),
            availability_status=state_data.get("availabilityStatus"),
            unavailable_reason=state_data.get("unavailableReason"),
            usage_mode=state_data.get("usageMode"),
            meta_received_at=state_data.get("metaReceivedAt"),
            meta_event_id=state_data.get("metaEventId"),
        ),
        meta=_parse_meta(data.get("meta", {})),
    )


def parse_battery_response(data: dict) -> BatteryTelemetryResponse:
    """Parse JSON response for battery telemetry endpoint."""
    state_data = data.get("data", {})
    return BatteryTelemetryResponse(
        data=BatteryState(
            vin=state_data.get("vin"),
            timestamp=_parse_timestamp(state_data.get("timestamp")),
            average_energy_consumption_kwh_per_100_km=state_data.get("averageEnergyConsumptionKwhPer100Km"),
            average_energy_consumption_kwh_per_100_km_automatic=state_data.get("averageEnergyConsumptionKwhPer100KmAutomatic"),
            average_energy_consumption_kwh_per_100_km_since_charge=state_data.get("averageEnergyConsumptionKwhPer100KmSinceCharge"),
            battery_charge_level_percentage=state_data.get("batteryChargeLevelPercentage"),
            charger_connection_status=state_data.get("chargerConnectionStatus"),
            charger_power_status=state_data.get("chargerPowerStatus"),
            charging_current_amps=state_data.get("chargingCurrentAmps"),
            charging_power_watts=state_data.get("chargingPowerWatts"),
            charging_status=state_data.get("chargingStatus"),
            charging_status_v2=state_data.get("chargingStatusV2"),
            charging_type=state_data.get("chargingType"),
            charging_voltage_volts=state_data.get("chargingVoltageVolts"),
            discharge_info=_parse_discharge_info(state_data.get("dischargeInfo")),
            energy_consumption_percentage_manual=_parse_energy_consumption_percentage(
                state_data.get("energyConsumptionPercentageManual")
            ),
            energy_consumption_percentage_automatic=_parse_energy_consumption_percentage(
                state_data.get("energyConsumptionPercentageAutomatic")
            ),
            energy_consumption_percentage_since_charge=_parse_energy_consumption_percentage(
                state_data.get("energyConsumptionPercentageSinceCharge")
            ),
            energy_consumption_wh_manual=_parse_energy_consumption_wh(
                state_data.get("energyConsumptionWhManual")
            ),
            energy_consumption_wh_automatic=_parse_energy_consumption_wh(
                state_data.get("energyConsumptionWhAutomatic")
            ),
            energy_consumption_wh_since_charge=_parse_energy_consumption_wh(
                state_data.get("energyConsumptionWhSinceCharge")
            ),
            estimated_charging_time_to_full_minutes=state_data.get("estimatedChargingTimeToFullMinutes"),
            estimated_charging_time_minutes_to_target_distance=state_data.get("estimatedChargingTimeMinutesToTargetDistance"),
            estimated_charging_time_minutes_to_minimum_soc=state_data.get("estimatedChargingTimeMinutesToMinimumSoc"),
            estimated_distance_to_empty_km=state_data.get("estimatedDistanceToEmptyKm"),
            estimated_distance_to_empty_miles=state_data.get("estimatedDistanceToEmptyMiles"),
            manual_preconditioning=_parse_manual_preconditioning(
                state_data.get("manualPreconditioning")
            ),
            total_energy_consumption_wh=state_data.get("totalEnergyConsumptionWh"),
            total_energy_consumption_wh_automatic=state_data.get("totalEnergyConsumptionWhAutomatic"),
            total_energy_consumption_wh_since_charge=state_data.get("totalEnergyConsumptionWhSinceCharge"),
            meta_received_at=state_data.get("metaReceivedAt"),
            meta_event_id=state_data.get("metaEventId"),
        ),
        meta=_parse_meta(data.get("meta", {})),
    )


def parse_exterior_response(data: dict) -> ExteriorTelemetryResponse:
    """Parse JSON response for exterior telemetry endpoint."""
    state_data = data.get("data", {})
    return ExteriorTelemetryResponse(
        data=ExteriorState(
            vin=state_data.get("vin"),
            timestamp=_parse_timestamp(state_data.get("timestamp")),
            central_lock=state_data.get("centralLock"),
            front_left_door=state_data.get("frontLeftDoor"),
            front_right_door=state_data.get("frontRightDoor"),
            rear_left_door=state_data.get("rearLeftDoor"),
            rear_right_door=state_data.get("rearRightDoor"),
            front_left_window=state_data.get("frontLeftWindow"),
            front_right_window=state_data.get("frontRightWindow"),
            rear_left_window=state_data.get("rearLeftWindow"),
            rear_right_window=state_data.get("rearRightWindow"),
            hood=state_data.get("hood"),
            fuel_flap=state_data.get("tankLid"),
            trunk=state_data.get("tailgate"),
            sunroof=state_data.get("sunroof"),
            alarm=state_data.get("alarm"),
            tailgate_lock=state_data.get("tailgateLock"),
            meta_received_at=state_data.get("metaReceivedAt"),
            meta_event_id=state_data.get("metaEventId"),
        ),
        meta=_parse_meta(data.get("meta", {})),
    )


def parse_health_response(data: dict) -> HealthTelemetryResponse:
    """Parse JSON response for health telemetry endpoint."""
    state_data = data.get("data", {})
    return HealthTelemetryResponse(
        data=HealthState(
            vin=state_data.get("vin"),
            timestamp=_parse_timestamp(state_data.get("timestamp")),
            engine_hours_to_service=state_data.get("engineHoursToService"),
            days_to_service=state_data.get("daysToService"),
            distance_to_service_km=state_data.get("distanceToServiceKm"),
            service_warning=state_data.get("serviceWarning"),
            brake_fluid_level_warning=state_data.get("brakeFluidLevelWarning"),
            engine_coolant_level_warning=state_data.get("engineCoolantLevelWarning"),
            oil_level_warning=state_data.get("oilLevelWarning"),
            washer_fluid_level_warning=state_data.get("washerFluidLevelWarning"),
            front_left_tyre_pressure_warning=state_data.get("frontLeftTyrePressureWarning"),
            front_right_tyre_pressure_warning=state_data.get("frontRightTyrePressureWarning"),
            rear_left_tyre_pressure_warning=state_data.get("rearLeftTyrePressureWarning"),
            rear_right_tyre_pressure_warning=state_data.get("rearRightTyrePressureWarning"),
            front_left_tyre_pressure_kpa=state_data.get("frontLeftTyrePressureKpa"),
            front_right_tyre_pressure_kpa=state_data.get("frontRightTyrePressureKpa"),
            rear_left_tyre_pressure_kpa=state_data.get("rearLeftTyrePressureKpa"),
            rear_right_tyre_pressure_kpa=state_data.get("rearRightTyrePressureKpa"),
            front_tyres_reference_pressure_kpa=state_data.get("frontTyresReferencePressureKpa"),
            rear_tyres_reference_pressure_kpa=state_data.get("rearTyresReferencePressureKpa"),
            low_voltage_battery_warning=state_data.get("lowVoltageBatteryWarning"),
            light_warnings=_parse_light_warnings(state_data.get("lightWarnings")),
            meta_received_at=state_data.get("metaReceivedAt"),
            meta_event_id=state_data.get("metaEventId"),
        ),
        meta=_parse_meta(data.get("meta", {})),
    )


def parse_location_response(data: dict) -> LocationTelemetryResponse:
    """Parse JSON response for location telemetry endpoint."""
    state_data = data.get("data", {})
    return LocationTelemetryResponse(
        data=LocationState(
            vin=state_data.get("vin"),
            timestamp=_parse_timestamp(state_data.get("timestamp")),
            altitude=state_data.get("altitude"),
            coordinate=_parse_coordinate(state_data.get("coordinate")),
            heading=state_data.get("heading"),
            speed=state_data.get("speed"),
            meta_received_at=state_data.get("metaReceivedAt"),
            meta_event_id=state_data.get("metaEventId"),
        ),
        meta=_parse_meta(data.get("meta", {})),
    )


def parse_odometer_response(data: dict) -> OdometerTelemetryResponse:
    """Parse JSON response for odometer telemetry endpoint."""
    state_data = data.get("data", {})
    return OdometerTelemetryResponse(
        data=OdometerState(
            vin=state_data.get("vin"),
            timestamp=_parse_timestamp(state_data.get("timestamp")),
            odometer_meters=state_data.get("odometerMeters"),
            trip_meter_manual_km=state_data.get("tripMeterManualKm"),
            average_speed_km_per_hour=state_data.get("averageSpeedKmPerHour"),
            trip_meter_automatic_km=state_data.get("tripMeterAutomaticKm"),
            average_speed_km_per_hour_automatic=state_data.get("averageSpeedKmPerHourAutomatic"),
            trip_meter_since_charge_km=state_data.get("tripMeterSinceChargeKm"),
            average_speed_km_per_hour_since_charge=state_data.get("averageSpeedKmPerHourSinceCharge"),
            meta_received_at=state_data.get("metaReceivedAt"),
            meta_event_id=state_data.get("metaEventId"),
        ),
        meta=_parse_meta(data.get("meta", {})),
    )


def parse_parking_climatization_response(data: dict) -> ParkingClimatizationTelemetryResponse:
    """Parse JSON response for parking climatization telemetry endpoint."""
    state_data = data.get("data", {})
    return ParkingClimatizationTelemetryResponse(
        data=ParkingClimatizationState(
            vin=state_data.get("vin"),
            timestamp=_parse_timestamp(state_data.get("timestamp")),
            running_status=state_data.get("runningStatus"),
            main_climate_running_status=state_data.get("mainClimateRunningStatus"),
            runtime_left_minutes=state_data.get("runtimeLeftMinutes"),
            errors=state_data.get("errors"),
            warnings=state_data.get("warnings"),
            ventilation=state_data.get("ventilation"),
            current_compartment_temperature_celsius=state_data.get("currentCompartmentTemperatureCelsius"),
            requested_compartment_temperature_celsius=state_data.get("requestedCompartmentTemperatureCelsius"),
            requested_front_left_seat=state_data.get("requestedFrontLeftSeat"),
            requested_front_right_seat=state_data.get("requestedFrontRightSeat"),
            requested_rear_left_seat=state_data.get("requestedRearLeftSeat"),
            requested_rear_right_seat=state_data.get("requestedRearRightSeat"),
            requested_steering_wheel_heating=state_data.get("requestedSteeringWheelHeating"),
            started_at=_parse_timestamp(state_data.get("startedAt")),
            ending_at=_parse_timestamp(state_data.get("endingAt")),
            start_reason=state_data.get("startReason"),
            meta_received_at=state_data.get("metaReceivedAt"),
            meta_event_id=state_data.get("metaEventId"),
        ),
        meta=_parse_meta(data.get("meta", {})),
    )


def parse_pre_cleaning_response(data: dict) -> PreCleaningTelemetryResponse:
    """Parse JSON response for pre-cleaning telemetry endpoint."""
    state_data = data.get("data", {})
    return PreCleaningTelemetryResponse(
        data=PreCleaningState(
            vin=state_data.get("vin"),
            timestamp=_parse_timestamp(state_data.get("timestamp")),
            last_cycle_completed=_parse_timestamp(state_data.get("lastCycleCompleted")),
            measurement_date=_parse_timestamp(state_data.get("measurementDate")),
            started_at=_parse_timestamp(state_data.get("startedAt")),
            ending_at=_parse_timestamp(state_data.get("endingAt")),
            running_status=state_data.get("runningStatus"),
            start_reason=state_data.get("startReason"),
            last_cycle_valid=state_data.get("lastCycleValid"),
            measured_air_quality_index=state_data.get("measuredAirQualityIndex"),
            measured_particulate_matter_25=state_data.get("measuredParticulateMatter25"),
            runtime_left_minutes=state_data.get("runtimeLeftMinutes"),
            error=state_data.get("error"),
            meta_received_at=state_data.get("metaReceivedAt"),
            meta_event_id=state_data.get("metaEventId"),
        ),
        meta=_parse_meta(data.get("meta", {})),
    )


# ---------------------------------------------------------------------------
# Charging parsers
# ---------------------------------------------------------------------------


def _parse_charging_meta(data: dict) -> ChargingMeta:
    return ChargingMeta(vin=data.get("vin"), domain=data.get("domain"))


def _parse_charging_timestamp(data: dict | None) -> ChargingTimestamp | None:
    if data is None:
        return None
    return ChargingTimestamp(
        seconds=data.get("seconds"),
        nanos=data.get("nanos"),
    )


def _parse_charging_coordinate(data: dict | None) -> ChargingCoordinate | None:
    if data is None:
        return None
    return ChargingCoordinate(
        latitude=data.get("latitude"),
        longitude=data.get("longitude"),
    )


def _parse_amp_limit_value(data: dict | None) -> AmpLimitValue | None:
    if data is None:
        return None
    return AmpLimitValue(
        amp_limit=data.get("ampLimit"),
        updated_at=data.get("updatedAt"),
        updated_at_timestamp=_parse_charging_timestamp(data.get("updatedAtTimestamp")),
        source=data.get("source"),
        id=data.get("id"),
    )


def _parse_charge_timer(data: dict | None) -> ChargeTimer | None:
    if data is None:
        return None
    return ChargeTimer(
        id=data.get("id"),
        activated=data.get("activated"),
        start=data.get("start"),
        stop=data.get("stop"),
        active_days=data.get("activeDays"),
    )


def _parse_charge_location(data: dict | None) -> ChargeLocation | None:
    if data is None:
        return None
    charge_timers = [_parse_charge_timer(t) for t in data.get("chargeTimers", [])] if data.get("chargeTimers") else None
    return ChargeLocation(
        metadata=data.get("metadata"),
        location_id=data.get("locationId"),
        location_alias=data.get("locationAlias"),
        coordinate=_parse_charging_coordinate(data.get("coordinate")),
        amp_limit=data.get("ampLimit"),
        minimum_soc=data.get("minimumSoc"),
        is_optimized_charging_enabled=data.get("isOptimizedChargingEnabled"),
        is_bidirectional_charging_enabled=data.get("isBidirectionalChargingEnabled"),
        available_optimized_charging=data.get("availableOptimizedCharging"),
        charge_timers=charge_timers,
        departure_times=data.get("departureTimes"),
        location_type=data.get("locationType"),
    )


def _parse_override_charge_timer_value(data: dict | None) -> OverrideChargeTimerValue | None:
    if data is None:
        return None
    return OverrideChargeTimerValue(
        override=data.get("override"),
        updated_at=data.get("updatedAt"),
        updated_at_timestamp=_parse_charging_timestamp(data.get("updatedAtTimestamp")),
    )


def _parse_global_charge_timer_value(data: dict | None) -> GlobalChargeTimerValue | None:
    if data is None:
        return None
    return GlobalChargeTimerValue(
        start=data.get("start"),
        stop=data.get("stop"),
        activated=data.get("activated"),
        metadata=data.get("metadata"),
    )


def _parse_timer_settings(data: dict | None) -> TimerSettings | None:
    if data is None:
        return None
    return TimerSettings(
        seat_heating_intensity=data.get("seatHeatingIntensity"),
        steering_wheel_heating_intensity=data.get("steeringWheelHeatingIntensity"),
        requested_compartment_temperature_celsius=data.get("requestedCompartmentTemperatureCelsius"),
        is_compartment_temperature_requested=data.get("isCompartmentTemperatureRequested"),
        battery_preconditioning=data.get("batteryPreconditioning"),
    )


def _parse_parking_climate_timer(data: dict | None) -> ParkingClimateTimer | None:
    if data is None:
        return None
    return ParkingClimateTimer(
        timer_id=data.get("timerId"),
        index=data.get("index"),
        ready_at=data.get("readyAt"),
        activated=data.get("activated"),
        repeat=data.get("repeat"),
        weekdays=data.get("weekdays"),
        start_date=data.get("startDate"),
        metadata=data.get("metadata"),
    )


def _parse_target_soc_value(data: dict | None) -> TargetSocValue | None:
    if data is None:
        return None
    return TargetSocValue(
        battery_charge_target_level=data.get("batteryChargeTargetLevel"),
        timestamp=_parse_charging_timestamp(data.get("timestamp")),
        charge_target_level_setting_type=data.get("chargeTargetLevelSettingType"),
        updated_at=data.get("updatedAt"),
        source=data.get("source"),
        id=data.get("id"),
    )


def parse_amp_limit_response(data: dict) -> AmpLimitTelemetryResponse:
    """Parse JSON response for amp limit charging endpoint."""
    state_data = data.get("data", {})
    return AmpLimitTelemetryResponse(
        data=AmpLimitState(
            vin=state_data.get("vin"),
            id=state_data.get("id"),
            updated_at=state_data.get("updatedAt"),
            updated_at_timestamp=_parse_charging_timestamp(state_data.get("updatedAtTimestamp")),
            amp_limit=_parse_amp_limit_value(state_data.get("ampLimit")),
            pending_amp_limit=_parse_amp_limit_value(state_data.get("pendingAmpLimit")),
            meta_received_at=state_data.get("metaReceivedAt"),
            meta_event_id=state_data.get("metaEventId"),
        ),
        meta=_parse_charging_meta(data.get("meta", {})),
    )


def parse_charge_locations_response(data: dict) -> ChargeLocationsTelemetryResponse:
    """Parse JSON response for charge locations charging endpoint."""
    state_data = data.get("data", {})
    charge_locations = [_parse_charge_location(loc) for loc in state_data.get("chargeLocations", [])] if state_data.get("chargeLocations") else None
    pending_charge_locations = [_parse_charge_location(loc) for loc in state_data.get("pendingChargeLocations", [])] if state_data.get("pendingChargeLocations") else None
    pending_delete = [_parse_charge_location(loc) for loc in state_data.get("pendingDeleteChargeLocations", [])] if state_data.get("pendingDeleteChargeLocations") else None
    return ChargeLocationsTelemetryResponse(
        data=ChargeLocationsState(
            vin=state_data.get("vin"),
            id=state_data.get("id"),
            charge_locations=charge_locations,
            pending_charge_locations=pending_charge_locations,
            pending_delete_charge_locations=pending_delete,
            utc0=state_data.get("utc0"),
            meta_received_at=state_data.get("metaReceivedAt"),
            meta_event_id=state_data.get("metaEventId"),
        ),
        meta=_parse_charging_meta(data.get("meta", {})),
    )


def parse_charge_now_response(data: dict) -> ChargeNowTelemetryResponse:
    """Parse JSON response for charge now (override charge timer) endpoint."""
    state_data = data.get("data", {})
    return ChargeNowTelemetryResponse(
        data=ChargeNowState(
            vin=state_data.get("vin"),
            id=state_data.get("id"),
            synced_override_charge_timer=_parse_override_charge_timer_value(
                state_data.get("syncedOverrideChargeTimer")
            ),
            pending_override_charge_timer=_parse_override_charge_timer_value(
                state_data.get("pendingOverrideChargeTimer")
            ),
            meta_received_at=state_data.get("metaReceivedAt"),
            meta_event_id=state_data.get("metaEventId"),
        ),
        meta=_parse_charging_meta(data.get("meta", {})),
    )


def parse_global_charge_timer_response(data: dict) -> GlobalChargeTimerTelemetryResponse:
    """Parse JSON response for global charge timer endpoint."""
    state_data = data.get("data", {})
    return GlobalChargeTimerTelemetryResponse(
        data=GlobalChargeTimerState(
            vin=state_data.get("vin"),
            id=state_data.get("id"),
            global_charge_timer=_parse_global_charge_timer_value(
                state_data.get("globalChargeTimer")
            ),
            pending_global_charge_timer=_parse_global_charge_timer_value(
                state_data.get("pendingGlobalChargeTimer")
            ),
            utc0=state_data.get("utc0"),
            meta_received_at=state_data.get("metaReceivedAt"),
            meta_event_id=state_data.get("metaEventId"),
        ),
        meta=_parse_charging_meta(data.get("meta", {})),
    )


def parse_is_at_charge_location_response(data: dict) -> IsAtChargeLocationResponse:
    """Parse JSON response for is-at-charge-location endpoint."""
    state_data = data.get("data", {})
    return IsAtChargeLocationResponse(
        data=IsAtChargeLocationState(
            vin=state_data.get("vin"),
            id=state_data.get("id"),
            location_id=state_data.get("locationId"),
            arrived_at=state_data.get("arrivedAt"),
            arrived_at_timestamp=_parse_charging_timestamp(state_data.get("arrivedAtTimestamp")),
            meta_received_at=state_data.get("metaReceivedAt"),
            meta_event_id=state_data.get("metaEventId"),
        ),
        meta=_parse_charging_meta(data.get("meta", {})),
    )


def parse_parking_climate_timer_response(data: dict) -> ParkingClimateTimerTelemetryResponse:
    """Parse JSON response for parking climate timer endpoint."""
    state_data = data.get("data", {})
    parking_climate_timers = [
        _parse_parking_climate_timer(t) for t in state_data.get("parkingClimateTimers", [])
    ] if state_data.get("parkingClimateTimers") else None
    pending_parking_climate_timers = [
        _parse_parking_climate_timer(t) for t in state_data.get("pendingParkingClimateTimers", [])
    ] if state_data.get("pendingParkingClimateTimers") else None
    pending_delete = [
        _parse_parking_climate_timer(t) for t in state_data.get("pendingDeleteParkingClimateTimers", [])
    ] if state_data.get("pendingDeleteParkingClimateTimers") else None
    return ParkingClimateTimerTelemetryResponse(
        data=ParkingClimateTimerState(
            vin=state_data.get("vin"),
            id=state_data.get("id"),
            updated_at=state_data.get("updatedAt"),
            updated_at_timestamp=_parse_charging_timestamp(state_data.get("updatedAtTimestamp")),
            parking_climate_timers=parking_climate_timers,
            pending_parking_climate_timers=pending_parking_climate_timers,
            pending_delete_parking_climate_timers=pending_delete,
            timer_settings=_parse_timer_settings(state_data.get("timerSettings")),
            pending_timer_settings=_parse_timer_settings(state_data.get("pendingTimerSettings")),
            utc0=state_data.get("utc0"),
            meta_received_at=state_data.get("metaReceivedAt"),
            meta_event_id=state_data.get("metaEventId"),
        ),
        meta=_parse_charging_meta(data.get("meta", {})),
    )


def parse_target_soc_response(data: dict) -> TargetSocTelemetryResponse:
    """Parse JSON response for target SoC charging endpoint."""
    state_data = data.get("data", {})
    return TargetSocTelemetryResponse(
        data=TargetSocState(
            vin=state_data.get("vin"),
            id=state_data.get("id"),
            updated_at=state_data.get("updatedAt"),
            timestamp=_parse_charging_timestamp(state_data.get("timestamp")),
            target_soc=_parse_target_soc_value(state_data.get("targetSoc")),
            pending_target_soc=_parse_target_soc_value(state_data.get("pendingTargetSoc")),
            meta_received_at=state_data.get("metaReceivedAt"),
            meta_event_id=state_data.get("metaEventId"),
        ),
        meta=_parse_charging_meta(data.get("meta", {})),
    )
