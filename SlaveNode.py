from concurrent import futures
import time, grpc, json

from proto import store_pb2_grpc, store_pb2

from proto.store import store_service

storeObj = {}


def main(port):
    store_service.set_store(storeObj)
    store_service.setNode("Slaves" + str(port))
    store_service.load_values()
    setMaster("localhost", port)

    time.sleep(1)
    start_grpc_server(port)
    
    while True:
        pass

#Sets a new client to the master's server
def setMaster(ip, port):
    master = "localhost:32770"  #Master will always use port 32770
    channel = grpc.insecure_channel(master) #Create a grpc channel to communicate with the master node

    stub = store_pb2_grpc.KeyValueStoreStub(channel)    #Obtain master's stub

    response = stub.discoverMsg(store_pb2.DiscoverMsgReq(ip=ip, port=port))
    data = response.data
    data = json.loads(data)
    #Take json data and store a client with it
    for key in data:
        store_service.store[key] = data[key]
        store_service.store_values(key, data[key])

#Start grpc connection
def start_grpc_server(port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    store_pb2_grpc.add_KeyValueStoreServicer_to_server(store_service, server)
    server.add_insecure_port("localhost:" + str(port))
    server.start()
    server.wait_for_termination()
