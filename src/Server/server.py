from concurrent.futures import ThreadPoolExecutor

from grpc import aio
from src.ANFIS.ANFIS import ANFIS
from src.ANFIS.MF import MF
from src.ANFIS.Term import Term
from src.Server.AnfisAnswerService import AnfisAnswerService
from src.Server.grpc import AnfisWorker_pb2_grpc


DEFAULT_HOST = "[::]"
DEFAULT_PORT = 50051

GREENHOUSE_RULES = [
    {"crop": "cucumber", "terms": ["middle", "high", "middle"], "coeffs": [0.006, 0.004, 0.00008], "free_coeff": 0.35},
    {"crop": "cucumber", "terms": ["high", "high", "middle"], "coeffs": [-0.004, 0.003, 0.00006], "free_coeff": 0.45},
    {"crop": "cucumber", "terms": ["low", "middle", "middle"], "coeffs": [0.004, 0.002, 0.00005], "free_coeff": 0.20},
    {"crop": "tomato", "terms": ["middle", "middle", "middle"], "coeffs": [0.007, 0.003, 0.00008], "free_coeff": 0.32},
    {"crop": "tomato", "terms": ["high", "middle", "high"], "coeffs": [-0.003, 0.002, 0.00005], "free_coeff": 0.48},
    {"crop": "tomato", "terms": ["low", "high", "middle"], "coeffs": [0.003, -0.002, 0.00005], "free_coeff": 0.30},
    {"crop": "berry", "terms": ["middle", "middle", "high"], "coeffs": [0.005, 0.003, 0.00004], "free_coeff": 0.38},
    {"crop": "berry", "terms": ["high", "low", "middle"], "coeffs": [-0.004, 0.002, 0.00004], "free_coeff": 0.30},
    {"crop": "berry", "terms": ["low", "high", "low"], "coeffs": [0.003, -0.003, 0.00003], "free_coeff": 0.28},
    {"crop": "greens", "terms": ["middle", "high", "low"], "coeffs": [0.004, 0.004, 0.00003], "free_coeff": 0.34},
    {"crop": "greens", "terms": ["low", "middle", "middle"], "coeffs": [0.003, 0.003, 0.00004], "free_coeff": 0.30},
    {"crop": "greens", "terms": ["high", "low", "high"], "coeffs": [-0.005, 0.002, 0.00003], "free_coeff": 0.28},
]


class Server:
    def __init__(
        self,
        host: str = DEFAULT_HOST,
        port: int = DEFAULT_PORT,
        anfis: ANFIS | None = None,
    ):
        self.host = host
        self.port = port
        self.anfis = anfis or self._build_default_anfis()
        self.server = None

    def register(self):
        self.server = aio.server(ThreadPoolExecutor(max_workers=10))
        self.server.add_insecure_port(f"{self.host}:{self.port}")

        answerService = AnfisAnswerService(anfis=self.anfis)
        AnfisWorker_pb2_grpc.add_NetAnswerServicer_to_server(answerService, server=self.server)

    @staticmethod
    def _build_default_anfis() -> ANFIS:
        fuzzyVariables = ["temperature", "humidity", "co2"]
        anfis: ANFIS = ANFIS(fuzzyVariables)
        termNames = ["low", "middle", "high"]
        temperatureTerms = {
            termNames[0]: Term(termNames[0]).setMembershipFunction(MF(10, 6)),
            termNames[1]: Term(termNames[1]).setMembershipFunction(MF(25, 6)),
            termNames[2]: Term(termNames[2]).setMembershipFunction(MF(40, 6))
        }
        anfis.addFuzzyVariableFromTerms(fuzzyVariables[0], temperatureTerms)

        humidityTerms = {
            termNames[0]: Term(termNames[0]).setMembershipFunction(MF(50, 5)),
            termNames[1]: Term(termNames[1]).setMembershipFunction(MF(75, 5)),
            termNames[2]: Term(termNames[2]).setMembershipFunction(MF(85, 5))
        }
        anfis.addFuzzyVariableFromTerms(fuzzyVariables[1], humidityTerms)

        co2Terms = {
            termNames[0]: Term(termNames[0]).setMembershipFunction(MF(200, 5)),
            termNames[1]: Term(termNames[1]).setMembershipFunction(MF(700, 5)),
            termNames[2]: Term(termNames[2]).setMembershipFunction(MF(1500, 5))
        }
        anfis.addFuzzyVariableFromTerms(fuzzyVariables[2], co2Terms)

        for rule in GREENHOUSE_RULES:
            anfis.addRule(
                rule["terms"],
                rule["coeffs"],
                rule["free_coeff"],
            )

        return anfis

    async def run(self):
        self.register()
        await self.server.start()
        try:
            await self.server.wait_for_termination()
        finally:
            await self.stop()
    
    async def stop(self, grace: float | None = 5.0):
        if self.server is not None:
            await self.server.stop(grace=grace)
            self.server = None
