import httpx

from src.core.exceptions import ExternalAPIError


class ArticClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def get_artwork(self, artwork_id: int) -> dict:
        try:
            response = httpx.get(
                f"{self.base_url}/artworks/{artwork_id}",
                timeout=10.0,
            )
        except httpx.HTTPError as e:
            raise ExternalAPIError(
                f"Failed to reach Art Institute API: {e}"
            ) from e

        if response.status_code == 404:
            raise ExternalAPIError(
                f"Artwork with id {artwork_id} not found in Art Institute API"
            )

        if response.status_code != 200:
            raise ExternalAPIError(
                f"Art Institute API returned status {response.status_code}"
            )

        return response.json()["data"]

    def search_artworks(
        self, query: str, page: int = 1, limit: int = 10
    ) -> dict:
        try:
            response = httpx.get(
                f"{self.base_url}/artworks/search",
                params={"q": query, "page": page, "limit": limit},
                timeout=10.0,
            )
        except httpx.HTTPError as e:
            raise ExternalAPIError(
                f"Failed to reach Art Institute API: {e}"
            ) from e

        if response.status_code != 200:
            raise ExternalAPIError(
                f"Art Institute API returned status {response.status_code}"
            )

        return response.json()
