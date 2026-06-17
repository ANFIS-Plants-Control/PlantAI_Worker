from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class SensorDatas(_message.Message):
    __slots__ = ("temperature", "humidity", "co2")
    TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    HUMIDITY_FIELD_NUMBER: _ClassVar[int]
    CO2_FIELD_NUMBER: _ClassVar[int]
    temperature: float
    humidity: float
    co2: float
    def __init__(self, temperature: _Optional[float] = ..., humidity: _Optional[float] = ..., co2: _Optional[float] = ...) -> None: ...

class ResponseValue(_message.Message):
    __slots__ = ("ans",)
    ANS_FIELD_NUMBER: _ClassVar[int]
    ans: float
    def __init__(self, ans: _Optional[float] = ...) -> None: ...
