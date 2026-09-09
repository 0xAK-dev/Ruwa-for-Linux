import json
import logging
from urllib import request

logger = logging.getLogger("RuwaInstaller")


def get_ruwa_versions() -> list | None:
    url = "https://api.github.com/repos/LuskusDeus/Ruwa-releases/releases?per_page=10"

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

