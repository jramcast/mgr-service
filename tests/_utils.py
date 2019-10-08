from unittest.mock import Mock
from asyncio import Future


def mock_resolves_to(value):
    future = Future()
    future.set_result(value)
    return Mock(return_value=future)
