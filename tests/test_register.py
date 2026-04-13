"""Tests for public registration action."""

import time

import pytest

from tests.test_client import CFMSTestClient


class TestRegister:
    @pytest.mark.asyncio
    async def test_register_success(self, client: CFMSTestClient):
        username = f"public_reg_{int(time.time() * 1000)}"
        password = "RegPassword123!"

        response = await client.send_request(
            "register",
            {
                "username": username,
                "password": password,
                "nickname": "Public User",
            },
            include_auth=False,
        )

        assert response.get("code") == 200, response

        login_response = await client.login(username, password)
        assert login_response.get("code") == 200, login_response

    @pytest.mark.asyncio
    async def test_register_duplicate_username(self, client: CFMSTestClient):
        username = f"public_dup_{int(time.time() * 1000)}"
        password = "RegPassword123!"

        first = await client.send_request(
            "register",
            {
                "username": username,
                "password": password,
            },
            include_auth=False,
        )
        assert first.get("code") == 200, first

        second = await client.send_request(
            "register",
            {
                "username": username,
                "password": password,
            },
            include_auth=False,
        )
        assert second.get("code") == 400, second
