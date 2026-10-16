"""Tests for the Polestar API authorization endpoint."""

from unittest.mock import MagicMock, patch

import pytest
import requests

from polestar_dpapi_client import PolestarClient, TokenResponse, AuthenticationError, ApiRequestError


class TestPolestarClientInit:
    """Tests for PolestarClient initialization."""

    def test_default_base_url(self):
        client = PolestarClient(app_client_id="test_id", client_secret="test_secret", client_header_id="test_header")
        assert client.base_url == PolestarClient.DEFAULT_BASE_URL

    def test_custom_base_url(self):
        client = PolestarClient(
            app_client_id="test_id",
            client_secret="test_secret",
            client_header_id="test_header",
            base_url="https://custom.api.com/m2m",
        )
        assert client.base_url == "https://custom.api.com/m2m"

    def test_token_is_none_initially(self):
        client = PolestarClient(app_client_id="test_id", client_secret="test_secret", client_header_id="test_header")
        assert client.token is None


class TestAuthenticate:
    """Tests for the authenticate method."""

    @patch("requests.Session.post")
    def test_successful_authentication(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "accessToken": "test-token-123",
            "expiresIn": 3600,
            "tokenType": "Bearer",
        }
        mock_post.return_value = mock_response

        client = PolestarClient(app_client_id="my_id", client_secret="my_secret", client_header_id="my_header")
        token = client.authenticate()

        assert isinstance(token, TokenResponse)
        assert token.access_token == "test-token-123"
        assert token.expires_in == 3600
        assert token.token_type == "Bearer"
        assert client.token is token

    @patch("requests.Session.post")
    def test_authentication_with_scope(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "accessToken": "test-token",
            "expiresIn": 3600,
            "tokenType": "Bearer",
        }
        mock_post.return_value = mock_response

        client = PolestarClient(app_client_id="my_id", client_secret="my_secret", client_header_id="my_header")
        client.authenticate(scope="pdp-telemetry/availability pdp-telemetry/battery")

        mock_post.assert_called_once()
        call_kwargs = mock_post.call_args[1]
        assert call_kwargs["json"]["scope"] == "pdp-telemetry/availability pdp-telemetry/battery"

    @patch("requests.Session.post")
    def test_authentication_sends_correct_payload(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "accessToken": "token",
            "expiresIn": 3600,
            "tokenType": "Bearer",
        }
        mock_post.return_value = mock_response

        client = PolestarClient(app_client_id="my_id", client_secret="my_secret", client_header_id="my_header")
        client.authenticate()

        call_kwargs = mock_post.call_args[1]
        assert call_kwargs["json"]["clientId"] == "my_id"
        assert call_kwargs["json"]["clientSecret"] == "my_secret"

    @patch("requests.Session.post")
    def test_401_raises_authentication_error(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.json.return_value = {
            "error": "invalid_client",
            "error_description": "Invalid client credentials",
            "timestamp": "2024-01-01T00:00:00Z",
        }
        mock_post.return_value = mock_response

        client = PolestarClient(app_client_id="bad_id", client_secret="bad_secret", client_header_id="bad_header")
        with pytest.raises(AuthenticationError, match="Invalid client credentials"):
            client.authenticate()

    @patch("requests.Session.post")
    def test_400_raises_authentication_error(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.json.return_value = {
            "error": "invalid_request",
            "error_description": "Missing required parameter",
            "timestamp": "2024-01-01T00:00:00Z",
        }
        mock_post.return_value = mock_response

        client = PolestarClient(app_client_id="id", client_secret="secret", client_header_id="header")
        with pytest.raises(AuthenticationError, match="Invalid token request"):
            client.authenticate()

    @patch("requests.Session.post")
    def test_500_raises_api_request_error(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.json.return_value = {
            "error": "server_error",
            "error_description": "Internal server error",
            "timestamp": "2024-01-01T00:00:00Z",
        }
        mock_post.return_value = mock_response

        client = PolestarClient(app_client_id="id", client_secret="secret", client_header_id="header")
        with pytest.raises(ApiRequestError, match="Internal server error"):
            client.authenticate()

    @patch("requests.Session.post")
    def test_502_raises_api_request_error(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 502
        mock_response.json.return_value = {
            "error": "bad_gateway",
            "error_description": "Invalid response from identity provider",
            "timestamp": "2024-01-01T00:00:00Z",
        }
        mock_post.return_value = mock_response

        client = PolestarClient(app_client_id="id", client_secret="secret", client_header_id="header")
        with pytest.raises(ApiRequestError, match="Identity provider error"):
            client.authenticate()

    @patch("requests.Session.post")
    def test_503_raises_api_request_error(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 503
        mock_response.json.return_value = {
            "error": "unavailable",
            "error_description": "Identity provider unavailable",
            "timestamp": "2024-01-01T00:00:00Z",
        }
        mock_post.return_value = mock_response

        client = PolestarClient(app_client_id="id", client_secret="secret", client_header_id="header")
        with pytest.raises(ApiRequestError, match="Identity provider error"):
            client.authenticate()

    @patch("requests.Session.post")
    def test_connection_error_raises_api_request_error(self, mock_post):
        mock_post.side_effect = requests.ConnectionError("Network unreachable")

        client = PolestarClient(app_client_id="id", client_secret="secret", client_header_id="header")
        with pytest.raises(ApiRequestError, match="Failed to connect"):
            client.authenticate()


class TestTokenResponse:
    """Tests for the TokenResponse model."""

    def test_headers_property(self):
        token = TokenResponse(
            access_token="abc123",
            expires_in=3600,
            token_type="Bearer",
        )
        headers = token.headers
        assert headers == {"Authorization": "Bearer abc123"}
