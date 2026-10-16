"""Tests for the Polestar API vehicles endpoint."""

from unittest.mock import MagicMock, patch

import pytest
import requests

from polestar_dpapi_client import (
    PolestarClient,
    TokenResponse,
    VehiclesListResponse,
    VehiclesMeta,
    AuthenticationError,
    ApiRequestError,
)


class TestListVehicles:
    """Tests for the list_vehicles method."""

    @patch("requests.Session.get")
    def test_successful_list_vehicles(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": ["YV1CZ000000000001", "LPSVS000000000002"],
            "meta": {"count": 2},
        }
        mock_get.return_value = mock_response

        client = PolestarClient(app_client_id="my_id", client_secret="my_secret", client_header_id="my_header")
        client._token = TokenResponse(
            access_token="test-token",
            expires_in=3600,
            token_type="Bearer",
        )

        result = client.list_vehicles()

        assert isinstance(result, VehiclesListResponse)
        assert result.data == ["YV1CZ000000000001", "LPSVS000000000002"]
        assert result.meta.count == 2

    @patch("requests.Session.get")
    def test_list_vehicles_sends_auth_headers(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": ["YV1CZ000000000001"],
            "meta": {"count": 1},
        }
        mock_get.return_value = mock_response

        client = PolestarClient(app_client_id="my_id", client_secret="my_secret", client_header_id="my_header")
        client._token = TokenResponse(
            access_token="test-token",
            expires_in=3600,
            token_type="Bearer",
        )

        client.list_vehicles()

        call_kwargs = mock_get.call_args[1]
        headers = call_kwargs["headers"]
        assert headers["Authorization"] == "Bearer test-token"
        assert headers["x-client-id"] == "my_header"

    @patch("requests.Session.get")
    def test_list_vehicles_with_delegated_account(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": ["YV1CZ000000000001"],
            "meta": {"count": 1},
        }
        mock_get.return_value = mock_response

        client = PolestarClient(app_client_id="my_id", client_secret="my_secret", client_header_id="my_header")
        client._token = TokenResponse(
            access_token="test-token",
            expires_in=3600,
            token_type="Bearer",
        )

        client.list_vehicles(delegated_account_id="jane.doe@acme.com")

        call_kwargs = mock_get.call_args[1]
        headers = call_kwargs["headers"]
        assert headers["x-delegated-account-id"] == "jane.doe@acme.com"

    def test_list_vehicles_raises_without_token(self):
        client = PolestarClient(app_client_id="my_id", client_secret="my_secret", client_header_id="my_header")
        with pytest.raises(AuthenticationError, match="No access token available"):
            client.list_vehicles()

    @patch("requests.Session.get")
    def test_400_raises_api_request_error(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.json.return_value = {
            "error": {
                "code": "INVALID_REQUEST",
                "message": "Invalid request parameters",
                "httpStatus": 400,
                "timestamp": "2024-01-01T00:00:00Z",
            }
        }
        mock_get.return_value = mock_response

        client = PolestarClient(app_client_id="my_id", client_secret="my_secret", client_header_id="my_header")
        client._token = TokenResponse(
            access_token="test-token",
            expires_in=3600,
            token_type="Bearer",
        )

        with pytest.raises(ApiRequestError, match="Invalid request parameters"):
            client.list_vehicles()

    @patch("requests.Session.get")
    def test_403_raises_api_request_error(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 403
        mock_response.json.return_value = {
            "error": {
                "code": "FORBIDDEN",
                "message": "No VIN authorization binding",
                "httpStatus": 403,
                "timestamp": "2024-01-01T00:00:00Z",
            }
        }
        mock_get.return_value = mock_response

        client = PolestarClient(app_client_id="my_id", client_secret="my_secret", client_header_id="my_header")
        client._token = TokenResponse(
            access_token="test-token",
            expires_in=3600,
            token_type="Bearer",
        )

        with pytest.raises(ApiRequestError, match="Forbidden"):
            client.list_vehicles()

    @patch("requests.Session.get")
    def test_503_raises_api_request_error(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 503
        mock_response.json.return_value = {
            "error": {
                "code": "SERVICE_UNAVAILABLE",
                "message": "Vehicle authorization provider unavailable",
                "httpStatus": 503,
                "timestamp": "2024-01-01T00:00:00Z",
            }
        }
        mock_get.return_value = mock_response

        client = PolestarClient(app_client_id="my_id", client_secret="my_secret", client_header_id="my_header")
        client._token = TokenResponse(
            access_token="test-token",
            expires_in=3600,
            token_type="Bearer",
        )

        with pytest.raises(ApiRequestError, match="Vehicle authorization provider unavailable"):
            client.list_vehicles()

    @patch("requests.Session.get")
    def test_connection_error_raises_api_request_error(self, mock_get):
        mock_get.side_effect = requests.ConnectionError("Network unreachable")

        client = PolestarClient(app_client_id="my_id", client_secret="my_secret", client_header_id="my_header")
        client._token = TokenResponse(
            access_token="test-token",
            expires_in=3600,
            token_type="Bearer",
        )

        with pytest.raises(ApiRequestError, match="Failed to connect"):
            client.list_vehicles()

    @patch("requests.Session.get")
    def test_empty_vehicles_list(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [],
            "meta": {"count": 0},
        }
        mock_get.return_value = mock_response

        client = PolestarClient(app_client_id="my_id", client_secret="my_secret", client_header_id="my_header")
        client._token = TokenResponse(
            access_token="test-token",
            expires_in=3600,
            token_type="Bearer",
        )

        result = client.list_vehicles()
        assert result.data == []
        assert result.meta.count == 0
