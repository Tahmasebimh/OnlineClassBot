from enum import Enum, auto


class AdminMode(Enum):
    SEND_HW = auto()
    SEND_CLASS_VIDEO = auto(),
    SEND_CLASS_VIDEO_TAG = auto(),
    PUBLIC_MESSAGE = auto(),
    UNKNOWN = auto()
