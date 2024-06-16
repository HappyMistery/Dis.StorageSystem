import os, store_pb2, time, random, json

#Class for centralized Slave nodes
class Store:
    def set_store(self, store):
        self.store = store

    #Load from file, save to store
    def load_values(self):
        try:
            os.makedirs("saves", exist_ok=True)
            file_path = os.path.join("saves", str(self.nodeType) + ".txt")
            file = open(file_path, "r")
            lines = file.readlines()
            for line in lines:
                parts = line.split(":")
                if len(parts) == 2:
                    self.store[parts[0]] = parts[1].replace("\n", "")
            file.close()
        except FileNotFoundError:   #If no file is found, we create one
            file = open(file_path, "w")
            file.close()

    #Store everything in a file
    def store_values(self, key, value):
        os.makedirs("saves", exist_ok=True)
        file_path = os.path.join("saves", str(self.nodeType) + ".txt")
        file = open(file_path, "a")
        file.write(key + ":" + value + "\n")
        file.close()

    def setNode(self, nodeType):
        self.nodeType = nodeType

    def __init__(self):
        self.store = {}
        self.slow_down_seconds = 0
        self.nodeType = random.randint(0, 1000000)  #Every node has a rand value

    def put(self, request, context):
        return store_pb2.PutResponse(success=False)

    def get(self, request, context):
        value = self.store.get(request.key)
        time.sleep(self.slow_down_seconds)
        if value is None:
            return store_pb2.GetResponse(value="", found=False)
        return store_pb2.GetResponse(value=value, found=True)

    #Set delay time to x given seconds
    def slowDown(self, request, context):
        try:
            self.seconds = request.seconds
            self.was_slowed = True
            while self.seconds > 0:
                time.sleep(1)
                self.seconds -= 1
            self.was_slowed = False
            return store_pb2.SlowDownResponse(success=True)
        except Exception as e:
            return store_pb2.SlowDownResponse(success=False)

    #Delay time restored to 0
    def restore(self, request, context):
        self.slow_down_seconds = 0
        return store_pb2.RestoreResponse(success=True)

    #If the node can commit
    def commit(self, request, context):
        time.sleep(self.slow_down_seconds)
        return store_pb2.CommitResp(success=True)

    #Node commits
    def finalCommit(self, request, context):
        self.store[request.key] = request.value
        self.store_values(request.key, request.value)
        return store_pb2.FinalCommitResp(success=True)

    def discoverMsg(self, request, context):
        return store_pb2.DiscoverMsgResp(data="")

    def votePut(self, request, context):
        time.sleep(self.slow_down_seconds)
        return store_pb2.VotePutResp(success=True, vote_size=self.vote_size)

    def voteGet(self, request, context):
        value = self.store.get(request.key)
        time.sleep(self.slow_down_seconds)
        if value is None:
            return store_pb2.VoteGetResp(
                success=False, vote_size=self.vote_size, value=""
            )
        return store_pb2.VoteGetResp(
            success=True, vote_size=self.vote_size, value=value
        )

    def parseJson(self):
        return json.dumps(self.store)

#Class for decentralized node
class NodeFunc(Store):
    def setVoteSize(self, vote_size):
        self.vote_size = vote_size

    def __init__(self):
        self.vote_size = 3
        super().__init__()

    #Get Request
    def get(self, request, context):
        import node
        value = node.handle_get_vote(
            request, self.store.get(request.key), self.vote_size
        )
        if value is None:
            return store_pb2.GetResponse(value="", found=False)
        return store_pb2.GetResponse(value=value, found=True)

    #Try to make a Put Request
    def put(self, request, context):
        import node
        #Call voting mechanism, if everything goes okay, return a good response
        if node.handle_put_vote(request):
            self.store[request.key] = request.value
            self.store_values(request.key, request.value)
            return store_pb2.PutResponse(success=True)
        #If Something goes wrong, return a bad response
        else:
            return store_pb2.PutResponse(success=False)


#Class for centralized Master node
class MasterService(Store):
    def setDiscoverQueue(self, discover_queue):
        self.discover_queue = discover_queue

    def __init__(self):
        super().__init__()

    #Master calls Two Phase Commit
    def put(self, request, context):
        import MasterNode
        #If evreything is okay, we give a good repsonse
        if MasterNode.two_phase_commit(self.store, request, context):
            self.store[request.key] = request.value

            self.store_values(request.key, request.value)
            return store_pb2.PutResponse(success=True)
        #If something goes wrong, we give a bad repsonse
        else:
            return store_pb2.PutResponse(success=False)

    def discoverMsg(self, request, context):
        self.discover_queue.append(request.ip + ":" + str(request.port))    #Add client's port and ip to clients list
        json_cont = json.dumps(self.store) 
        return store_pb2.DiscoverMsgResp(data=json_cont)    #Return a json with clients list contents


node_service = NodeFunc()
master_service = MasterService()
store_service = Store()
