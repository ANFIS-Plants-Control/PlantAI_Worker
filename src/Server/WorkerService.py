from src.Server.grpc.worker_pb2_grpc import WorkerServiceServicer
from src.Server.grpc import worker_pb2

class WorkerService(WorkerServiceServicer):
    async def GetData(self, request, context):
        print('aaaaaaaaaaaaaaaa')
        print(request)
        return worker_pb2.DataResponse(responseId=1,
    data=1.0,
    SensorType=1)