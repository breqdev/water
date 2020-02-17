import socket
import message
from select import select

class Server:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.connections = [self.sock]
        self.waiting = []

        self.uuids = {}

    def bind(self, port):
        self.sock.bind(("0.0.0.0", port))
        self.sock.listen(16)

    def remove(self, sock):
        try:
            sock.close()
        except:
            pass
        if sock in self.connections:
            self.connections.remove(sock)
        if sock in self.waiting:
            self.waiting.remove(sock)

        # inform others
        newmsg = message.Message().withParams(
            "WatrSrvr", {"water":["client_left"]},
            (self.uuids[sock] if sock in self.uuids else "unknown"))

        self.broadcast(newmsg)

        if sock in self.uuids:
            del self.uuids[sock]

    def broadcast(self, msg):
        for s in self.connections:
            if s is not self.sock:
                print("Broadcast: sending to socket")
                try:
                    s.send(msg.dumps().encode("UTF-8"))
                except Exception as e:
                    self.remove(s)
                    

    def handleEvents(self):
        read_sockets = select(self.connections+self.waiting, [], [], 0)[0]

        for sock in read_sockets:
            if sock == self.sock:
                newsock, addr = self.sock.accept()
                print(f"Accepting new socket at {addr} to waiting")

                self.waiting.append(newsock)

            else:
                try:
                    data = sock.recv(4096)
                    addr = sock.getpeername()

                    print(f"Received data from {addr}: {data.decode('UTF-8')}")

                    if sock in self.waiting:
                        msg = message.Message()
                        if msg.fromJSON(data.decode("UTF-8")):
                            if "handshake" in msg.tags["water"]:
                                self.connections.append(sock)
                                print(f"Socket at {addr} has passed handshake")

                                self.uuids[sock] = msg.sender

                                # send "new socket" message
                                newmsg = message.Message().withParams(
                                    "WatrSrvr", {"water":["client_joined"]},
                                    msg.sender)

                                self.broadcast(newmsg)
                                self.waiting.remove(sock)
                                print(f"Removing socket {addr} from waiting")
                                continue

                                
                        self.remove(sock)
                        print(f"Removing socket {addr}, failed handshake")
                        continue

                    if data:
                        msg = message.Message()
                        if msg.fromJSON(data.decode("UTF-8")):
                            print(f"Forwarding message from socket {addr}")
                            self.broadcast(msg)
                    else:
                        print("Received empty data, closing socket")
                        raise ValueError("empty data")
                except Exception as e:
                    print(f"Exception with socket")
                    print(e)
                    self.remove(sock)
                            
if __name__ == "__main__":
    s = Server()
    s.bind(8888)
    while True:
        s.handleEvents()
