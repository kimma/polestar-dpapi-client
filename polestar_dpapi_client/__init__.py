"""
Polestar API - A Python module for interfacing with the Polestar data platform.

This module provides tools and utilities for interacting with the official
Polestar data platform API.
"""

from polestar_dpapi_client.api.client import PolestarClient
from polestar_dpapi_client.exceptions import AuthenticationError, ApiRequestError, PolestarAPIError
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

__version__ = "1.0.0"
__author__ = "Kim-Eirik Karlsen"
__all__ = [
    "PolestarClient",
    "TokenResponse",
    "VehiclesListResponse",
    "VehiclesMeta",
    "PolestarAPIError",
    "AuthenticationError",
    "ApiRequestError",
    # Telemetry
    "TelemetryTimestamp",
    "TelemetryCoordinate",
    "TelemetryMeta",
    "AvailabilityState",
    "AvailabilityTelemetryResponse",
    "EnergyConsumptionPercentage",
    "EnergyConsumptionWh",
    "DischargeInfo",
    "ManualPreconditioning",
    "BatteryState",
    "BatteryTelemetryResponse",
    "ExteriorState",
    "ExteriorTelemetryResponse",
    "LightWarnings",
    "HealthState",
    "HealthTelemetryResponse",
    "LocationState",
    "LocationTelemetryResponse",
    "OdometerState",
    "OdometerTelemetryResponse",
    "ParkingClimatizationState",
    "ParkingClimatizationTelemetryResponse",
    "PreCleaningState",
    "PreCleaningTelemetryResponse",
]
