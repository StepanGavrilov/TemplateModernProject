"""
CRUD
"""

import orjson
import httpx

from unittest import IsolatedAsyncioTestCase
from dotenv import dotenv_values
from fastapi import status
from fastapi.testclient import TestClient

from asgi import app

config = dotenv_values(".env")
client = TestClient(app)

API = f'{config.get("API_HOST")}:{config.get("API_PORT")}'
USERNAME = "TheTestUserNameNumberOne1251"
PASSWORD = "TheTestPasswordNumberOne8"
JWT_AUTH = ''


class Account_01_TestCreate(IsolatedAsyncioTestCase):  # NOSONAR

    def setUp(self) -> None:
        self.jwt = None

    def test_account_creation(self):
        response = httpx.post(
            url=f"http://{API}/account/",  # NOSONAR
            content=orjson.dumps({
                "username": USERNAME,
                "password": PASSWORD
            })
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
            f"Account not created,"
            f" status: {response.status_code, response.content}"
        )

        JWT_AUTH = orjson.loads(response.content). \
            get("detail").get("access_token")

        self.assertIsNotNone(
            JWT_AUTH,
            f"No valid access token: {JWT_AUTH}"
        )
        self.assertIsInstance(
            JWT_AUTH,
            str,
            f"Not valid access token type: {type(JWT_AUTH)}"
        )


class Account_02_TestCreateDuplicate(IsolatedAsyncioTestCase):  # NOSONAR
    """
    Diplicate username
    """

    def setUp(self) -> None:
        self.jwt = None

    def test_account_creation_username_duplicate(self):
        response = httpx.post(
            url=f"http://{API}/account/",  # NOSONAR
            content=orjson.dumps({
                "username": USERNAME,
                "password": PASSWORD
            })
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_409_CONFLICT,
            "Account not duplicated"
        )
        error_message = orjson.loads(
            response.content
        ).get("detail").get("message")

        self.assertEqual(
            error_message,
            "Account with this username or email already exists.",
            "Error message not actual."
        )


class Account_03_TestLogin(IsolatedAsyncioTestCase):  # NOSONAR

    def setUp(self) -> None:
        self.jwt = None

    def test_account_login(self):
        with httpx.Client() as client:
            response = client.post(
                f"http://{API}/account/login/",  # NOSONAR
                content=orjson.dumps({
                    "username": USERNAME,
                    "password": PASSWORD
                })
            )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            f"Login failed: {response.status_code}"
        )
        message = orjson.loads(response.content).get("detail").get("message")
        global JWT_AUTH
        JWT_AUTH = str(orjson.loads(response.content).
                       get("detail").get("token"))
        self.assertIsNotNone(
            JWT_AUTH,
            f"Not access token {JWT_AUTH}"
        )
        self.assertEqual(
            message,
            "Authenticated successfully",
            f"Login message failed: {message}"
        )


class Account_04_TestUpdate(IsolatedAsyncioTestCase):  # NOSONAR
    def test_account_update(self):
        with httpx.Client() as client:
            response = client.put(
                headers={"Authorization": f"Bearer {JWT_AUTH}"},
                url=f"http://{API}/account/",  # NOSONAR
                content=orjson.dumps({
                    "job": "programmer",
                })
            )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            f'response: {response.status_code, response.content, JWT_AUTH}'
        )


class Account_05_TestDelete(IsolatedAsyncioTestCase):  # NOSONAR
    def test_account_delete(self):
        with httpx.Client() as client:
            response = client.delete(
                headers={"Authorization": f"Bearer {JWT_AUTH}"},
                url=f"http://{API}/account/",  # NOSONAR
            )
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
            f'response: {response.status_code, response.content, JWT_AUTH}'
        )
