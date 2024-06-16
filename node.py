import grpc, random, socket, sys, json
from concurrent import futures

sys.path.append("proto")
from proto import store_pb2_grpc, store_pb2
from proto.store import node_service

global global_vote
global_vote = 1

get_size = 2
put_size = 3
local = ""
discovered_ports = []

#Listens to all braodcasts and respons with its information if it recieves one. It stores whatever info it recieves from the responses
def listen(socket):
    while True:
        socket_info, addr = socket.recvfrom(1024)
        if socket_info.startswith(b"Discovery;"):   #Discovery messages start with the string "Discovery"
            div = socket_info.decode().split(";")
            if len(div) == 2 and div[0] == "Discovery":
                port_discovered = div[1]
                port_found = False
                for port in discovered_ports:
                    if port == port_discovered:
                        port_found = True
                        break
                if not port_found:
                    discovered_ports.append(port_discovered)
                    response = "DiscoveryResponse;*;" + node_service.parseJson()    #Response messages start with the string "DiscoveryResponse"
                    socket.sendto(response.encode(), addr)
        elif socket_info.startswith(b"DiscoveryResponse;"):
            div = socket_info.decode().split(";*;")
            if div[0] == "DiscoveryResponse" and len(div) == 2:
                socket_info = div[1]
                socket_info = json.loads(socket_info)
                for key in socket_info:
                    node_service.store[key] = socket_info[key]
                    node_service.store_values(key, socket_info[key])

#Sends a broadcast to ports 30000-31000
def send(port_discovered, sock):
    for port in range(30000, 31000):
        sock.sendto(
            b"Discovery;" + bytes(port_discovered, "utf-8"), ("255.255.255.255", port)
        )

#Starts grpc server
def start_grpc_server(port):
    channelServer = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    store_pb2_grpc.add_KeyValueStoreServicer_to_server(node_service, channelServer)
    print(f"Server is listening on port {port}")
    channelServer.add_insecure_port("localhost:" + str(port))
    channelServer.start()
    channelServer.wait_for_termination()

#Sends a vote request to all nodes
def handle_get_vote(requestG, val, valSize):
    values = {}
    values[val] = valSize
    for ipport in discovered_ports:
        if ipport == local:
            continue
        channel = grpc.insecure_channel(ipport) #Call every node with grpc
        stub = store_pb2_grpc.KeyValueStoreStub(channel)
        commit = store_pb2.VoteGetReq(key=requestG.key) #Make every node vote the request
        stored = stub.voteGet(commit)
        if stored.success:  #Check node's response to the request
            if stored.value in values:
                current_value = values[stored.value]
                values[stored.value] = current_value + stored.vote_size
            else:
                values[stored.value] = stored.vote_size
    valMax = val
    voteMax = valSize
    for key in values:
        if values[key] > voteMax:
            voteMax = values[key]
            valMax = key
    if voteMax >= get_size: #No consensus if not enough positive votes gathered
        return valMax
    else:
        return None

#Starts a votation to make a put
def handle_put_vote(requestP):
    votesCount = 0
    for port in discovered_ports:
        if port == local:
            current_count = votesCount
            votesCount = current_count + global_vote
            continue
        channel = grpc.insecure_channel(port)   #Call every node with grpc
        stub = store_pb2_grpc.KeyValueStoreStub(channel)
        requestOb = store_pb2.VotePutReq(key=requestP.key, value=requestP.value)    #Make every node vote the request
        stored = stub.votePut(requestOb)
        if stored.success:  #Check node's response to the request
            current_count = votesCount
            votesCount = current_count + stored.vote_size
    if votesCount >= put_size:
        for port in discovered_ports:
            channel = grpc.insecure_channel(port)
            stub = store_pb2_grpc.KeyValueStoreStub(channel)
            commit = store_pb2.FinalCommitReq(key=requestP.key, value=requestP.value)   #Make every node make a commit
            stored = stub.finalCommit(commit)
            if not stored.success:  #If any node fails, everything stops and no commit is done.
                return False
        return True
    else:
        return False


def main(port):
    global global_vote
    port_socket = 30000 + random.randint(0, 1000)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("", port_socket))    #Starts braodcast listener
    listener_thread = futures.ThreadPoolExecutor(max_workers=1)
    listener_thread.submit(listen, sock)
    local = "localhost:" + str(port)
    node_service.setNode("Node" + str(port))
    node_service.load_values()
    send(local, sock)
    if port == 32771:
        node_service.setVoteSize(2)
        global_vote = 2
    else:
        node_service.setVoteSize(1)
        global_vote = 1

    start_grpc_server(port)
