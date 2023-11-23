import pytest
from ..src.protocol import *


@pytest.mark.parametrize("buffer, expected", [
    (b"+Par", (None, 0)),
    (b"+OK\r\n", (SimpleString("OK"), 5)),
    (b"+OK\r\n+Next", (SimpleString("OK"), 5)),
])
def test_read_frame_simple_string(buffer, expected):
    actual = extract_frame_from_buffer(buffer)
    assert actual == expected

@pytest.mark.parametrize("buffer, expected", [
    ("-Error message\r\n", Error("Error message"), 12), 
])
def test_read_frame_error(buffer, expected):
    actual = extract_frame_from_buffer(buffer)
    assert actual == expected


@pytest.mark.parametrize("buffer, expected", [
    (":1\r\n", 1),
    (":1\r\n:2\r\n", 1)
])
def test_read_frame_integer(buffer, expected):
    actual = extract_frame_from_buffer(buffer)
    assert actual == expected


@pytest.parametrize("buffer", "expected", [
    ("$5\r\nhello\r\n", BulkString("hello"), 5),
    ("$0\r\n\r\n", BulkString(""), 0)
])
def test_read_frame_bulk_string(buffer, expected):
    actual = extract_frame_from_buffer(buffer)
    assert actual == expected