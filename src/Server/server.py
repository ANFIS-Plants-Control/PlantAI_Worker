from concurrent.futures import ThreadPoolExecutor

from grpc import aio

from src.Server.WorkerService import WorkerService
from src.Server.grpc import worker_pb2_grpc

class Server:
    def __init__(self):
        pass

    def register(self):
        self.server = aio.server(ThreadPoolExecutor(max_workers=10))
        self.server.add_insecure_port(f'[::]:{50051}')
        worker_pb2_grpc.add_WorkerServiceServicer_to_server(WorkerService(), self.server)

    async def run(self):
        self.register()
        await self.server.start()
        await self.server.wait_for_termination()
    
    async def stop(self):
        await self.server.stop(grace=False)