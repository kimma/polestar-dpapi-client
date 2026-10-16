"""Vehicle-related models for Polestar API responses."""

from dataclasses import dataclass


@dataclass
class VehiclesMeta:
    """Metadata for a vehicles list response.

    Attributes:
        count: Number of VINs returned.
    """

    count: int


@dataclass
class VehiclesListResponse:
    """Response from GET /v1/vehicles.

    Attributes:
        data: List of VINs the authenticated caller is authorized to access.
        meta: Metadata about the response.
    """

    data: list[str]
    meta: VehiclesMeta
