import json
import time
from typing import Any

from websockets import ConnectionClosed


from include.classes.client import LockableClientConnection
from include.util.connect import get_connection
from main import AppConfig

# from include.function.lockdown import go_lockdown


async def do_request(
    action: str,
    data: dict = {},
    message: str = "",
    username=None,
    token=None,
    max_retries: int = 3,
) -> dict:
    _app_config = AppConfig()
    _conn = _app_config.get_not_none_attribute("conn")

    assert max_retries >= 1, "max_retries must be at least 1"

    response: dict[str, Any] = {}
    for attempt in range(max_retries):
        try:
            response = await _request(
                _conn,
                action,
                data,
                message,
                username=username,
                token=token,
            )
        except (ConnectionClosed, ConnectionAbortedError, ConnectionResetError):
            if attempt >= max_retries - 1:
                raise
            _conn = await get_connection(_app_config.server_address)
            _app_config.conn = _conn
            continue

        break

    return response


async def _request(
    conn: LockableClientConnection,
    action: str,
    data: dict = {},
    message: str = "",
    username=None,
    token=None,
) -> dict:

    request = {
        "action": action,
        "data": data,
        "username": username,
        "token": token,
        "timestamp": time.time(),
    }

    request_json = json.dumps(request, ensure_ascii=False)

    async with conn.lock:
        await conn.send(request_json)
        response = await conn.recv()

    loaded_response: dict = json.loads(response)
    return loaded_response
