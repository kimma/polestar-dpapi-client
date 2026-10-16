"""
Data models for Polestar API responses.
"""

from polestar_dpapi_client.models.token import TokenResponse
from polestar_dpapi_client.models.vehicles import VehiclesListResponse, VehiclesMeta
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

__all__ = [
    # Token
    "TokenResponse",
    # Vehicles
    "VehiclesListResponse",
    "VehiclesMeta",
    # Telemetry - shared types
    "TelemetryTimestamp",
    "TelemetryCoordinate",
    "TelemetryMeta",
    # Telemetry - availability
    "AvailabilityState",
    "AvailabilityTelemetryResponse",
    # Telemetry - battery
    "EnergyConsumptionPercentage",
    "EnergyConsumptionWh",
    "DischargeInfo",
    "ManualPreconditioning",
    "BatteryState",
    "BatteryTelemetryResponse",
    # Telemetry - exterior
    "ExteriorState",
    "ExteriorTelemetryResponse",
    # Telemetry - health
    "LightWarnings",
    "HealthState",
    "HealthTelemetryResponse",
    # Telemetry - location
    "LocationState",
    "LocationTelemetryResponse",
    # Telemetry - odometer
    "OdometerState",
    "OdometerTelemetryResponse",
    # Telemetry - parking climatization
    "ParkingClimatizationState",
    "ParkingClimatizationTelemetryResponse",
    # Telemetry - pre-cleaning
    "PreCleaningState",
    "PreCleaningTelemetryResponse",
]
