import threading, MasterNode, SlaveNode

#Starts a single thread for the master node 
def start_master_thread():
    def run_master():
        print("Starting master node")
        MasterNode.main()

    master_thread = threading.Thread(target=run_master)
    master_thread.start()
    return master_thread

#Starts two threads, one for every slave node
def start_slave_threads():
    ports = [32771, 32772]

    def run_slave(port):
        print(f"Starting slave node on port: {port}")
        SlaveNode.main(port)

    threads = []
    for port in ports:  #Every slave node has a port associated. We run this for every port/slave
        slave_thread = threading.Thread(target=run_slave, args=(port,))
        slave_thread.start()
        threads.append(slave_thread)

    return threads

#Initiate master node and slave nodes
master_thread = start_master_thread()
slave_threads = start_slave_threads()

all_threads = [master_thread] + slave_threads
#Wait for every thread to end
for thread in all_threads:
    thread.join()

#Keep the program running
while True:
    pass
