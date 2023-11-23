import pytest
from dataclasses import dataclass

MSG_SEPARATOR = b"\r\n"

@dataclass
class SimpleString:
    data: str

def extract_frame_from_buffer(buffer):
    match chr(buffer[0]):
        case '+':
            separator = buffer.find(MSG_SEPARATOR)

            if separator != -1:
                return SimpleString(buffer[1:separator].decode()), separator + 2
        
    return None, 0

@pytest.mark.parametrize("buffer, expected", [
    (b"+Par", (None, 0)),
    (b"+OK\r\n", (SimpleString("OK"), 5)),
    (b"+OK\r\n+Next", (SimpleString("OK"), 5)),
])

def test_read_frame_simple_string(buffer, expected):
    actual = extract_frame_from_buffer(buffer)
    assert actual == expected

