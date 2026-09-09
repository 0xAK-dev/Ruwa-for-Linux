import json
import logging
from urllib import request

logger = logging.getLogger("RuwaInstaller")


def get_ruwa_versions(limit: int =10) -> list[str] | None:
    """
    Get the latest Ruwa release versions from GitHub.
    
    Args:
        limit: Maximum number of releases to retrieve. Defaults to 10.

    Returns:
        A list of release version tags, such as
        ["0.3.1-alpha", "0.3.0-alpha"].
        Returns None if the GitHub request fails.
    """
    url = f"https://api.github.com/repos/LuskusDeus/Ruwa-releases/releases?per_page={limit}"

    with request.urlopen(url=url) as data:
        if data.status == 200:
            releases = json.loads(data.read())

            logger.info("Successfully got version")
            tags = [
                release.get("tag_name")
                for release in releases
                if release.get("tag_name")
            ]

            return tags

        logger.error("Failed to get version: HTTP status code %s", data.status)

        return None

