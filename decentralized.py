import threading,node

#Start 3 threads, one for every decentralized node.
node_ports = [32770, 32771, 32772]

def start_node(port):
    print(f"Decentralized node on port {port} started")
    node.main(port)

threads = []
for port in node_ports: #Every node has a port associated. We run this for every port/node
    node_thread = threading.Thread(target=start_node, args=(port,))
    node_thread.start()
    threads.append(node_thread)

#Wait for every thread/node to finalize
for thread in threads:
    thread.join()

#Keep the program running
while True:
    pass