import logging
import urllib.request

from settings import settings

logger = logging.getLogger(__name__)


def run_healthcheck():
    """Run healthcheck against the API."""
    port = settings.APP_PORT
    api_v1 = settings.API_V1_STR
    try:
        with urllib.request.urlopen(
            f"http://localhost:{port}{api_v1}/health"
        ) as response:
            if response.status == 200:
                return True
            return False
    except Exception as e:
        logger.exception("Healthcheck failed: %s", e)

    return False


if __name__ == "__main__":
    run_healthcheck()
