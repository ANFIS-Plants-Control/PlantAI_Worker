import logging

import grpc
from src.Server.grpc.AnfisWorker_pb2_grpc import NetAnswerServicer
from src.Server.grpc import AnfisWorker_pb2


logger = logging.getLogger(__name__)


class AnfisAnswerService(NetAnswerServicer):
    def __init__(self, anfis):
        super().__init__()
        self.anfis = anfis

    async def GetNetAnswer(self, request, context):
        input_data = self._request_to_input_data(request)

        try:
            self.anfis.computeAllFuzzyVariables(input_data)
            answer, _ = self.anfis.forward(input_data)
        except Exception:
            logger.exception("Failed to calculate ANFIS answer")
            await context.abort(
                grpc.StatusCode.INTERNAL,
                "Failed to calculate ANFIS answer",
            )

        return AnfisWorker_pb2.ResponseValue(ans=float(answer))

    @staticmethod
    def _request_to_input_data(request: AnfisWorker_pb2.SensorDatas) -> dict[str, float]:
        return {
            "temperature": float(request.temperature),
            "humidity": float(request.humidity),
            "co2": float(request.co2),
        }
