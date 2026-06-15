from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class GetDataRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class DataResponse(_message.Message):
    __slots__ = ("responseId", "data", "SensorType")
    RESPONSEID_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    SENSORTYPE_FIELD_NUMBER: _ClassVar[int]
    responseId: int
    data: float
    SensorType: int
    def __init__(self, responseId: _Optional[int] = ..., data: _Optional[float] = ..., SensorType: _Optional[int] = ...) -> None: ...
