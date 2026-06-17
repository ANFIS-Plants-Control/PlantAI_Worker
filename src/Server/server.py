from concurrent.futures import ThreadPoolExecutor
from grpc import aio
from src.ANFIS.MF import MF
from src.ANFIS.Term import Term
from src.Server import AnfisAnswerService
from src.Server.grpc import AnfisWorker_pb2_grpc
from src.ANFIS.ANFIS import ANFIS

class Server:
    def __init__(self):
        pass

    def register(self):
        self.server = aio.server(ThreadPoolExecutor(max_workers=10))
        self.server.add_insecure_port(f'[::]:{50051}')

        fuzzyVariables = ['temperature', 'humidity', 'co2']
        anfis:ANFIS = ANFIS(fuzzyVariables)
        termNames = ["low", 'middle', 'high']
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

        answerService:AnfisAnswerService = AnfisAnswerService
        AnfisWorker_pb2_grpc.add_NetAnswerServicer_to_server(answerService)

    async def run(self):
        self.register()
        await self.server.start()
        await self.server.wait_for_termination()
    
    async def stop(self):
        await self.server.stop(grace=False)