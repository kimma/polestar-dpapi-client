"""Polestar API client for interfacing with the Polestar data platform."""

import requests
from polestar_dpapi_client.exceptions import AuthenticationError, ApiRequestError
from polestar_dpapi_client.models.token import TokenResponse
from polestar_dpapi_client.models.vehicles import VehiclesListResponse, VehiclesMeta
from polestar_dpapi_client.models.telemetry import (
    AvailabilityTelemetryResponse,
    BatteryTelemetryResponse,
    ExteriorTelemetryResponse,
    HealthTelemetryResponse,
    LocationTelemetryResponse,
    OdometerTelemetryResponse,
    ParkingClimatizationTelemetryResponse,
    PreCleaningTelemetryResponse,
    TelemetryMeta,
)
from polestar_dpapi_client.models.charging import (
    AmpLimitTelemetryResponse,
    ChargeLocationsTelemetryResponse,
    ChargeNowTelemetryResponse,
    GlobalChargeTimerTelemetryResponse,
    IsAtChargeLocationResponse,
    ParkingClimateTimerTelemetryResponse,
    TargetSocTelemetryResponse,
)
from polestar_dpapi_client.utils.telemetry_parser import (
    parse_availability_response,
    parse_battery_response,
    parse_exterior_response,
    parse_health_response,
    parse_location_response,
    parse_odometer_response,
    parse_parking_climatization_response,
    parse_pre_cleaning_response,
    parse_amp_limit_response,
    parse_charge_locations_response,
    parse_charge_now_response,
    parse_global_charge_timer_response,
    parse_is_at_charge_location_response,
    parse_parking_climate_timer_response,
    parse_target_soc_response,
)


class PolestarClient:
    """Client for the Polestar M2M data platform API.

    Args:
        app_client_id: The client ID obtained from the Polestar developer portal.
        client_secret: The client secret obtained from the Polestar developer portal.
        client_header_id: The client header ID for API requests.
        base_url: The base URL for the M2M API. Defaults to the EU North-1 endpoint.

    Example:
        >>> client = PolestarClient(
        ...     app_client_id="my_id",
        ...     client_secret="my_secret",
        ...     client_header_id="my_header_id",
        ... )
        >>> token = client.authenticate()
        >>> print(token.access_token)
    """

    DEFAULT_BASE_URL = "https://pc-api.polestar.com/eu-north-1/data-portal/m2m"

    def __init__(
        self,
        app_client_id: str,
        client_secret: str,
        client_header_id: str,
        base_url: str | None = None,
    ):
        self.app_client_id = app_client_id
        self.client_secret = client_secret
        self.client_header_id = client_header_id
        self.base_url = base_url or self.DEFAULT_BASE_URL
        self._token: TokenResponse | None = None
        self._session = requests.Session()

    def authenticate(self, scope: str | None = None) -> TokenResponse:
        """Authenticate with the Polestar M2M API and obtain an access token.

        Args:
            scope: Optional space-separated OAuth scopes to request.
                Supported scopes include:
                - pdp-telemetry/availability
                - pdp-telemetry/battery
                - pdp-telemetry/exterior
                - pdp-telemetry/health
                - pdp-telemetry/location
                - pdp-telemetry/odometer
                - pdp-telemetry/parkingClimatization
                - pdp-telemetry/preCleaning
                - pdp-charging/ampLimit
                - pdp-charging/chargeLocations
                - pdp-charging/overrideChargeTimer
                - pdp-charging/globalChargeTimer
                - pdp-charging/isAtChargeLocation
                - pdp-charging/parkingClimateTimer
                - pdp-charging/targetSoc

        Returns:
            TokenResponse containing the access token, expiry, and token type.

        Raises:
            AuthenticationError: If credentials are invalid or the identity provider rejects the request.
            ApiRequestError: If the API request fails for another reason.
        """
        payload = {
            "clientId": self.app_client_id,
            "clientSecret": self.client_secret,
        }
        if scope:
            payload["scope"] = scope

        try:
            response = self._session.post(
                f"{self.base_url}/token",
                json=payload,
                headers={"Content-Type": "application/json"},
            )
        except requests.RequestException as exc:
            raise ApiRequestError(f"Failed to connect to Polestar API: {exc}") from exc

        if response.status_code == 400:
            error_body = self._parse_error(response)
            raise AuthenticationError(
                f"Invalid token request: {error_body}",
                status_code=response.status_code,
            )
        if response.status_code == 401:
            error_body = self._parse_error(response)
            raise AuthenticationError(
                f"Invalid client credentials: {error_body}",
                status_code=response.status_code,
            )
        if response.status_code in (502, 503):
            error_body = self._parse_error(response)
            raise ApiRequestError(
                f"Identity provider error: {error_body}",
                status_code=response.status_code,
            )
        if response.status_code == 500:
            error_body = self._parse_error(response)
            raise ApiRequestError(
                f"Internal server error: {error_body}",
                status_code=response.status_code,
            )

        response.raise_for_status()

        data = response.json()
        token = TokenResponse(
            access_token=data["accessToken"],
            expires_in=data["expiresIn"],
            token_type=data["tokenType"],
        )
        self._token = token
        return token

    @property
    def token(self) -> TokenResponse | None:
        """Return the current token, if one has been obtained."""
        return self._token

    def list_vehicles(
        self,
        delegated_account_id: str | None = None,
    ) -> VehiclesListResponse:
        """List the VINs the authenticated caller is authorized to access.

        Requires a valid access token. Call :meth:`authenticate` first if no
        token has been obtained yet.

        Args:
            delegated_account_id: Third-party credentials only. The account
                (email) whose shared VINs you want to access. The account must
                belong to the same company domain as the credential. When
                omitted, VINs are resolved for the account that created the
                credential.

        Returns:
            VehiclesListResponse containing the list of authorized VINs and
            metadata.

        Raises:
            AuthenticationError: If no valid token is available.
            ApiRequestError: If the API request fails.
        """
        if self._token is None:
            raise AuthenticationError(
                "No access token available. Call authenticate() first.",
                status_code=None,
            )

        headers = {
            **self._token.headers,
            "x-client-id": self.client_header_id,
        }
        if delegated_account_id:
            headers["x-delegated-account-id"] = delegated_account_id

        try:
            response = self._session.get(
                f"{self.base_url}/v1/vehicles",
                headers=headers,
            )
        except requests.RequestException as exc:
            raise ApiRequestError(f"Failed to connect to Polestar API: {exc}") from exc

        if response.status_code == 400:
            error_body = self._parse_m2m_error(response)
            raise ApiRequestError(
                f"Invalid request parameters: {error_body}",
                status_code=response.status_code,
            )
        if response.status_code == 403:
            error_body = self._parse_m2m_error(response)
            raise ApiRequestError(
                f"Forbidden: no VIN authorization binding configured: {error_body}",
                status_code=response.status_code,
            )
        if response.status_code == 503:
            error_body = self._parse_m2m_error(response)
            raise ApiRequestError(
                f"Vehicle authorization provider unavailable: {error_body}",
                status_code=response.status_code,
            )

        response.raise_for_status()

        data = response.json()
        return VehiclesListResponse(
            data=data["data"],
            meta=VehiclesMeta(count=data["meta"]["count"]),
        )

    # ------------------------------------------------------------------
    # Telemetry helpers
    # ------------------------------------------------------------------

    def _get_telemetry(
        self,
        path: str,
        delegated_account_id: str | None = None,
    ) -> dict:
        """Execute an authenticated GET request to a telemetry endpoint.

        Args:
            path: The API path (e.g. ``/v1/vehicles/{vin}/telemetry/battery``).
            delegated_account_id: Optional delegated account identifier.

        Returns:
            Parsed JSON payload as a dictionary.

        Raises:
            AuthenticationError: If no valid token is available.
            ApiRequestError: If the API request fails.
        """
        if self._token is None:
            raise AuthenticationError(
                "No access token available. Call authenticate() first.",
                status_code=None,
            )

        headers = {
            **self._token.headers,
            "x-client-id": self.client_header_id,
        }
        if delegated_account_id:
            headers["x-delegated-account-id"] = delegated_account_id

        try:
            response = self._session.get(
                f"{self.base_url}{path}",
                headers=headers,
            )
        except requests.RequestException as exc:
            raise ApiRequestError(f"Failed to connect to Polestar API: {exc}") from exc

        if response.status_code == 400:
            error_body = self._parse_m2m_error(response)
            raise ApiRequestError(
                f"Invalid request parameters: {error_body}",
                status_code=response.status_code,
            )
        if response.status_code == 403:
            error_body = self._parse_m2m_error(response)
            raise ApiRequestError(
                f"Forbidden: {error_body}",
                status_code=response.status_code,
            )
        if response.status_code == 404:
            error_body = self._parse_m2m_error(response)
            raise ApiRequestError(
                f"Vehicle or telemetry endpoint not found: {error_body}",
                status_code=response.status_code,
            )
        if response.status_code == 429:
            error_body = self._parse_m2m_error(response)
            raise ApiRequestError(
                f"Rate limit exceeded: {error_body}",
                status_code=response.status_code,
            )
        if response.status_code == 503:
            error_body = self._parse_m2m_error(response)
            raise ApiRequestError(
                f"Service unavailable: {error_body}",
                status_code=response.status_code,
            )

        response.raise_for_status()
        return response.json()

    # ------------------------------------------------------------------
    # Telemetry endpoints
    # ------------------------------------------------------------------

    def get_availability(
        self,
        vin: str,
        delegated_account_id: str | None = None,
    ) -> AvailabilityTelemetryResponse:
        """Fetch availability state for a vehicle.

        Returns availability status, usage mode, and unavailability reason.

        Args:
            vin: The vehicle identification number.
            delegated_account_id: Optional delegated account identifier.

        Returns:
            AvailabilityTelemetryResponse containing the availability state.

        Raises:
            AuthenticationError: If no valid token is available.
            ApiRequestError: If the API request fails.
        """
        data = self._get_telemetry(
            f"/v1/vehicles/{vin}/telemetry/availability",
            delegated_account_id=delegated_account_id,
        )
        return parse_availability_response(data)

    def get_battery(
        self,
        vin: str,
        delegated_account_id: str | None = None,
    ) -> BatteryTelemetryResponse:
        """Fetch battery state for a vehicle.

        Returns charge level, charging status, range estimates, and energy
        consumption breakdowns.

        Args:
            vin: The vehicle identification number.
            delegated_account_id: Optional delegated account identifier.

        Returns:
            BatteryTelemetryResponse containing the battery state.

        Raises:
            AuthenticationError: If no valid token is available.
            ApiRequestError: If the API request fails.
        """
        data = self._get_telemetry(
            f"/v1/vehicles/{vin}/telemetry/battery",
            delegated_account_id=delegated_account_id,
        )
        return parse_battery_response(data)

    def get_exterior(
        self,
        vin: str,
        delegated_account_id: str | None = None,
    ) -> ExteriorTelemetryResponse:
        """Fetch exterior state for a vehicle.

        Returns door, lock, window, hood, fuel flap, and trunk status.

        Args:
            vin: The vehicle identification number.
            delegated_account_id: Optional delegated account identifier.

        Returns:
            ExteriorTelemetryResponse containing the exterior state.

        Raises:
            AuthenticationError: If no valid token is available.
            ApiRequestError: If the API request fails.
        """
        data = self._get_telemetry(
            f"/v1/vehicles/{vin}/telemetry/exterior",
            delegated_account_id=delegated_account_id,
        )
        return parse_exterior_response(data)

    def get_health(
        self,
        vin: str,
        delegated_account_id: str | None = None,
    ) -> HealthTelemetryResponse:
        """Fetch health state for a vehicle.

        Returns service warnings, trip meters, fluid levels, and light
        warning indicators.

        Args:
            vin: The vehicle identification number.
            delegated_account_id: Optional delegated account identifier.

        Returns:
            HealthTelemetryResponse containing the health state.

        Raises:
            AuthenticationError: If no valid token is available.
            ApiRequestError: If the API request fails.
        """
        data = self._get_telemetry(
            f"/v1/vehicles/{vin}/telemetry/health",
            delegated_account_id=delegated_account_id,
        )
        return parse_health_response(data)

    def get_location(
        self,
        vin: str,
        delegated_account_id: str | None = None,
    ) -> LocationTelemetryResponse:
        """Fetch current location coordinates for a vehicle.

        Returns latitude, longitude, altitude, heading, and speed.

        Args:
            vin: The vehicle identification number.
            delegated_account_id: Optional delegated account identifier.

        Returns:
            LocationTelemetryResponse containing the location state.

        Raises:
            AuthenticationError: If no valid token is available.
            ApiRequestError: If the API request fails.
        """
        data = self._get_telemetry(
            f"/v1/vehicles/{vin}/telemetry/location",
            delegated_account_id=delegated_account_id,
        )
        return parse_location_response(data)

    def get_odometer(
        self,
        vin: str,
        delegated_account_id: str | None = None,
    ) -> OdometerTelemetryResponse:
        """Fetch odometer readings for a vehicle.

        Returns total odometer, trip meters, and average speed.

        Args:
            vin: The vehicle identification number.
            delegated_account_id: Optional delegated account identifier.

        Returns:
            OdometerTelemetryResponse containing the odometer state.

        Raises:
            AuthenticationError: If no valid token is available.
            ApiRequestError: If the API request fails.
        """
        data = self._get_telemetry(
            f"/v1/vehicles/{vin}/telemetry/odometer",
            delegated_account_id=delegated_account_id,
        )
        return parse_odometer_response(data)

    def get_parking_climatization(
        self,
        vin: str,
        delegated_account_id: str | None = None,
    ) -> ParkingClimatizationTelemetryResponse:
        """Fetch parking climatization state for a vehicle.

        Returns running status, temperatures, seat heating, and timers.

        Args:
            vin: The vehicle identification number.
            delegated_account_id: Optional delegated account identifier.

        Returns:
            ParkingClimatizationTelemetryResponse containing the parking
            climatization state.

        Raises:
            AuthenticationError: If no valid token is available.
            ApiRequestError: If the API request fails.
        """
        data = self._get_telemetry(
            f"/v1/vehicles/{vin}/telemetry/parking-climatization",
            delegated_account_id=delegated_account_id,
        )
        return parse_parking_climatization_response(data)

    def get_pre_cleaning(
        self,
        vin: str,
        delegated_account_id: str | None = None,
    ) -> PreCleaningTelemetryResponse:
        """Fetch cabin pre-cleaning state for a vehicle.

        Returns air quality index, PM2.5, running status, and cycle info.

        Args:
            vin: The vehicle identification number.
            delegated_account_id: Optional delegated account identifier.

        Returns:
            PreCleaningTelemetryResponse containing the pre-cleaning state.

        Raises:
            AuthenticationError: If no valid token is available.
            ApiRequestError: If the API request fails.
        """
        data = self._get_telemetry(
            f"/v1/vehicles/{vin}/telemetry/pre-cleaning",
            delegated_account_id=delegated_account_id,
        )
        return parse_pre_cleaning_response(data)

    # ------------------------------------------------------------------
    # Charging endpoints
    # ------------------------------------------------------------------

    def get_amp_limit(
        self,
        vin: str,
        delegated_account_id: str | None = None,
    ) -> AmpLimitTelemetryResponse:
        """Fetch amp limit state for a vehicle.

        Returns the configured amp limit and pending amp limit.

        Args:
            vin: The vehicle identification number.
            delegated_account_id: Optional delegated account identifier.

        Returns:
            AmpLimitTelemetryResponse containing the amp limit state.

        Raises:
            AuthenticationError: If no valid token is available.
            ApiRequestError: If the API request fails.
        """
        data = self._get_telemetry(
            f"/v1/vehicles/{vin}/charging/amp-limit",
            delegated_account_id=delegated_account_id,
        )
        return parse_amp_limit_response(data)

    def get_charge_locations(
        self,
        vin: str,
        delegated_account_id: str | None = None,
    ) -> ChargeLocationsTelemetryResponse:
        """Fetch charge locations state for a vehicle.

        Returns configured charge locations, pending locations, and deletion queue.

        Args:
            vin: The vehicle identification number.
            delegated_account_id: Optional delegated account identifier.

        Returns:
            ChargeLocationsTelemetryResponse containing the charge locations state.

        Raises:
            AuthenticationError: If no valid token is available.
            ApiRequestError: If the API request fails.
        """
        data = self._get_telemetry(
            f"/v1/vehicles/{vin}/charging/charge-locations",
            delegated_account_id=delegated_account_id,
        )
        return parse_charge_locations_response(data)

    def get_charge_now(
        self,
        vin: str,
        delegated_account_id: str | None = None,
    ) -> ChargeNowTelemetryResponse:
        """Fetch charge now (override charge timer) state for a vehicle.

        Returns the override charge timer status.

        Args:
            vin: The vehicle identification number.
            delegated_account_id: Optional delegated account identifier.

        Returns:
            ChargeNowTelemetryResponse containing the charge now state.

        Raises:
            AuthenticationError: If no valid token is available.
            ApiRequestError: If the API request fails.
        """
        data = self._get_telemetry(
            f"/v1/vehicles/{vin}/charging/charge-now",
            delegated_account_id=delegated_account_id,
        )
        return parse_charge_now_response(data)

    def get_global_charge_timer(
        self,
        vin: str,
        delegated_account_id: str | None = None,
    ) -> GlobalChargeTimerTelemetryResponse:
        """Fetch global charge timer state for a vehicle.

        Returns the global charge timer configuration.

        Args:
            vin: The vehicle identification number.
            delegated_account_id: Optional delegated account identifier.

        Returns:
            GlobalChargeTimerTelemetryResponse containing the global charge timer state.

        Raises:
            AuthenticationError: If no valid token is available.
            ApiRequestError: If the API request fails.
        """
        data = self._get_telemetry(
            f"/v1/vehicles/{vin}/charging/global-charge-timer",
            delegated_account_id=delegated_account_id,
        )
        return parse_global_charge_timer_response(data)

    def get_is_at_charge_location(
        self,
        vin: str,
        delegated_account_id: str | None = None,
    ) -> IsAtChargeLocationResponse:
        """Fetch is-at-charge-location state for a vehicle.

        Returns whether the vehicle is currently at a charge location.

        Args:
            vin: The vehicle identification number.
            delegated_account_id: Optional delegated account identifier.

        Returns:
            IsAtChargeLocationResponse containing the is-at-charge-location state.

        Raises:
            AuthenticationError: If no valid token is available.
            ApiRequestError: If the API request fails.
        """
        data = self._get_telemetry(
            f"/v1/vehicles/{vin}/charging/is-at-charge-location",
            delegated_account_id=delegated_account_id,
        )
        return parse_is_at_charge_location_response(data)

    def get_parking_climate_timer(
        self,
        vin: str,
        delegated_account_id: str | None = None,
    ) -> ParkingClimateTimerTelemetryResponse:
        """Fetch parking climate timer state for a vehicle.

        Returns parking climate timers and timer settings.

        Args:
            vin: The vehicle identification number.
            delegated_account_id: Optional delegated account identifier.

        Returns:
            ParkingClimateTimerTelemetryResponse containing the parking climate timer state.

        Raises:
            AuthenticationError: If no valid token is available.
            ApiRequestError: If the API request fails.
        """
        data = self._get_telemetry(
            f"/v1/vehicles/{vin}/charging/parking-climate-timer",
            delegated_account_id=delegated_account_id,
        )
        return parse_parking_climate_timer_response(data)

    def get_target_soc(
        self,
        vin: str,
        delegated_account_id: str | None = None,
    ) -> TargetSocTelemetryResponse:
        """Fetch target state of charge state for a vehicle.

        Returns the target SoC configuration.

        Args:
            vin: The vehicle identification number.
            delegated_account_id: Optional delegated account identifier.

        Returns:
            TargetSocTelemetryResponse containing the target SoC state.

        Raises:
            AuthenticationError: If no valid token is available.
            ApiRequestError: If the API request fails.
        """
        data = self._get_telemetry(
            f"/v1/vehicles/{vin}/charging/target-soc",
            delegated_account_id=delegated_account_id,
        )
        return parse_target_soc_response(data)

    def _parse_error(self, response: requests.Response) -> str:
        """Extract error description from an OAuth2 error response."""
        try:
            data = response.json()
            return data.get("error_description", data.get("error", "Unknown error"))
        except (ValueError, KeyError):
            return response.text or "No error details provided"

    def _parse_m2m_error(self, response: requests.Response) -> str:
        """Extract error description from an M2M API error response."""
        try:
            data = response.json()
            error = data.get("error", {})
            return error.get("message", "Unknown error")
        except (ValueError, KeyError):
            return response.text or "No error details provided"
