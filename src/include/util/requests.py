import json
import time
from typing import Any

from websockets import ConnectionClosed
from websockets.asyncio.client import ClientConnection
from include.util.connect import get_connection
from include.classes.config import AppConfig
import asyncio
import weakref

# from include.function.lockdown import go_lockdown

# store locks per-connection without attaching them to the connection object
_conn_locks = weakref.WeakKeyDictionary()


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


def _get_conn_lock(conn: ClientConnection) -> asyncio.Lock:
    lock = _conn_locks.get(conn)
    if lock is None:
        lock = asyncio.Lock()
        _conn_locks[conn] = lock
    return lock


async def _request(
    conn: ClientConnection,
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

    lock = _get_conn_lock(conn)
    async with lock:
        await conn.send(request_json)
        response = await conn.recv()

    loaded_response: dict = json.loads(response)
    return loaded_response
