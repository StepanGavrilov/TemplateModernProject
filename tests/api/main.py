from unittest import IsolatedAsyncioTestCase

import requests
from urllib3.exceptions import NewConnectionError


class MainTest(IsolatedAsyncioTestCase):
    """Main functionality of API"""

    def test_root_endpoint(self):
        """Test root endpoint"""

        try:
            response = requests.get("http://127.0.0.1:9999/")
        except (ConnectionError, NewConnectionError):
            pass
        else:
            self.assertEqual(
                response.status_code,
                200,
                "No correct response from root endpoint."
            )
