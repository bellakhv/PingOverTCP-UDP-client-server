# !/usr/local/bin/python2.7

import threading
from struct import *

dataLen = 1000000

'''
This class holds all the information about the connection for simpler use. 
'''
class Connection:

    def __init__(self, hostname, port, protocol, timeout=1, packetSize=32, count=4):
        self.hostname = hostname
        self.port = port
        self.protocol = protocol
        self.timeout = timeout
        self.packetSize = packetSize
        self.count = count

'''
This class extends threading thread and implement a new thread for incoming TCP connection.
When close connection from client received the thread is exiting
'''
class ClientThread(threading.Thread):

    def __init__(self,clientAddress,clientSocket):
        threading.Thread.__init__(self)
        self.clientSocket = clientSocket
        self.clientAddress = clientAddress
        print ("New connection added: ", clientAddress)

    def run(self):
        print ("Connection from : ", self.clientAddress)
        while True:
            data = self.clientSocket.recv(dataLen)
            msg_type, seqNum = unpack("!ii", data)
            if seqNum == 0:
                break
            data = pack('!ii', 2, seqNum)
            self.clientSocket.sendall(data)
        print ("Client at ", self.clientAddress , " disconnected...")
        self.clientSocket.close()
