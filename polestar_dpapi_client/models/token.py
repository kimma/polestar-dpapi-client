"""Token response model for Polestar API authorization."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class TokenResponse:
    """Represents an OAuth2 token response from the Polestar M2M API.

    Attributes:
        access_token: The bearer token to use for authenticated requests.
        expires_in: Token validity duration in seconds.
        token_type: The type of token (e.g., "Bearer").
    """

    access_token: str
    expires_in: int
    token_type: str

    @property
    def headers(self) -> dict[str, str]:
        """Return authorization headers suitable for passing to requests."""
        return {"Authorization": f"{self.token_type} {self.access_token}"}
