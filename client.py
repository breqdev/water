import socket
from select import select
import time
import uuid

import message

class Client:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.uuid = uuid.uuid4()

    def makeMessage(self, tags, content):
        msg = message.Message()
        msg.withParams(str(self.uuid), tags, content)
        return msg

    def sendMessage(self, msg):
        #print(f"Sending message {msg.dumps()}")
        self.sock.send(msg.dumps().encode("UTF-8"))

    def connect(self, host, port=8888):
        self.sock.connect((host, port))

        connMessage = self.makeMessage({"water":["handshake"]}, "")
        self.sendMessage(connMessage)

    def getMessages(self):
        msgs = []
        if select([self.sock], [], [], 0)[0] == [self.sock]:
            recv = self.sock.recv(4096).decode("UTF-8")

            parts = recv.split("\x00")
            
            for part in parts:
                msg = message.Message()
                if msg.fromJSON(part):
                    msgs.append(msg)
                else:
                    #print("Error Receiving Message")
                    #print(part)
                    pass

            return msgs
                    
        else:
            pass #print("No Messages To Receive")

    def close(self):
        self.sock.close()
            
            
if __name__ == "__main__":
    c = Client()
    c.connect("localhost")
    time.sleep(1)
    c.sendMessage(c.makeMessage({"chat":["message"]}, "test"))
    time.sleep(1)
    print(c.getMessages()[0].dumps())
    time.sleep(1)
    c.close()
