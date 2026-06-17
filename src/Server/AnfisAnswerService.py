from src.Server.grpc.AnfisWorker_pb2_grpc import NetAnswerServicer
from src.Server.grpc import AnfisWorker_pb2

class AnfisAnswerService(NetAnswerServicer):
    def __init__(self, anfis):
        super().__init__()
        self.anfis = anfis

    async def GetNetAnswer(self, request, context):
        data = request
        AnfisWorker_pb2.ResponseValue(1)
