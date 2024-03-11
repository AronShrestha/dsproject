from asyncio import futures
from concurrent import futures

import grpc
from bootstrap import init_database, init_queue, init_broadcaster

# from krispcall.billing.entrypoints.grpc import workspace_credit_pb2_grpc
# from krispcall.billing.entrypoints.grpc.server import WorkspaceCredit


from redis import Redis


async def server(settings):
    """Start async grpc server"""
    server_ = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    db = init_database(settings)
    queue = init_queue(settings)
    # await db.connect()
    await queue.connect()
    broadcaster = init_broadcaster(settings)
    await broadcaster.connect()
    # workspace_credit_pb2_grpc.add_WorkspaceCreditServicer_to_server(
    #     WorkspaceCredit(db), server_
    # )
    server_.add_insecure_port("[::]:8003")
    await server_.start()
    await server_.wait_for_termination()
