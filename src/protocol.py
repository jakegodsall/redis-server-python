from dataclasses import dataclass

MSG_SEPARATOR = b"\r\n"

@dataclass
class SimpleString:
    data: str

@dataclass
class Error:
    data: str

@dataclass
class Integer:
    data: int

@dataclass
class BulkString:
    data: str

def extract_frame_from_buffer(buffer):
    match chr(buffer[0]):
        case '+':
            separator = buffer.find(MSG_SEPARATOR)

            if separator != -1:
                return SimpleString(buffer[1:separator].decode()), separator + 2
        
    return None, 0