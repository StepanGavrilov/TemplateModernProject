import requests

from unittest import IsolatedAsyncioTestCase

from requests import RequestException
from dotenv import dotenv_values

config = dotenv_values(".env")


class MainTest(IsolatedAsyncioTestCase):
    """Main functionality of API"""

    def test_root_endpoint(self):
        """Test root endpoint"""

        try:
            response = requests.get(
                f"http://{config.get('API_HOST')}:{config.get('API_PORT')}/"
            )
        except RequestException:
            return False

        self.assertIsInstance(
            response,
            requests.models.Response,
            f"No response. {type(response)}"
        )
        self.assertEqual(
            response.status_code,
            200,
            "No correct response from root endpoint."
        )
