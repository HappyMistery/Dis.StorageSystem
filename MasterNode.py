import grpc, time
from concurrent import futures

try:
    from proto import store_pb2_grpc, store_pb2
    from proto.store import master_service
except:
    import sys

    sys.path.append("proto")
    from proto import store_pb2_grpc, store_pb2
from proto.store import master_service

discoveredPorts = []
storeObj = {}


def main():
    master_service.set_store(storeObj)
    master_service.setNode("Master" + str(32770))   #Default port for master node must be 32770
    master_service.load_values()
    master_service.setDiscoverQueue(discoveredPorts)
    start_grpc_server()

    while True:
        time.sleep(60)
        pass

#Two Phase Commit started by Master node
def two_phase_commit(self, request, context):
    try:
        #Let all the nodes say they can make the commit
        for port in discoveredPorts:
            channel = grpc.insecure_channel(port)
            stub = store_pb2_grpc.KeyValueStoreStub(channel)

            finalCommit = store_pb2.CommitReq(key=request.key, value=request.value)
            stored = stub.commit(finalCommit)
            if not stored.success:
                return False
        #Let all the nodes do the commit
        for port in discoveredPorts:
            channel = grpc.insecure_channel(port)
            stub = store_pb2_grpc.KeyValueStoreStub(channel)
            finalCommit = store_pb2.FinalCommitReq(key=request.key, value=request.value)
            stored = stub.finalCommit(finalCommit)
            if not stored.success:
                return False
        return True
    except: #If a node fails to accept the commit, we stop the 2pc and don't do the commit.
        return False

#Start grpc connection
def start_grpc_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    store_pb2_grpc.add_KeyValueStoreServicer_to_server(master_service, server)
    server.add_insecure_port("localhost:32770") #Open connection through Master's port
    server.start()
    server.wait_for_termination()
