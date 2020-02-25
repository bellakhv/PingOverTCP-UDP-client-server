#!/usr/local/bin/python2.7

'''
This script creates a server that listen for TCP and UDP connections on a specific port;
Using select() the server knows on witch port there is incoming request
'''

from socket import *
from struct import *
from utils import ClientThread
from select import select
import random

# IP and Port for the server to listen on
SERVER_IP = '127.0.0.1'
PORT = 2001
dataLen = 1000000
CLIENTS_NUM = 10

#For testing the server when TEST=1
TEST_MODE = 1
THRESHOLD = 5

serverUdpSocket = socket(AF_INET, SOCK_DGRAM)
serverTcpSocket = socket(AF_INET, SOCK_STREAM)

serverUdpSocket.bind((SERVER_IP, PORT))
serverTcpSocket.bind((SERVER_IP, PORT+1))

print("The server is ready to receive on port %d for UDP, and %d for TCP" %(PORT, PORT+1))



while True:

    # if random picked int smaller that threshold replay will send otherwise the message will be dropped.
    if TEST_MODE == 1:
        drop = random.randint(1, 10)
    else:
        drop = 1

    serverTcpSocket.listen(CLIENTS_NUM)
    input = [serverTcpSocket, serverUdpSocket]
    inputready, outputready, exceptready = select(input, [], [])

    for s in inputready:
        if s is serverTcpSocket:
            connection, clientAddress = serverTcpSocket.accept()
            newThread = ClientThread(clientAddress, connection)
            newThread.start()

        elif s is serverUdpSocket:
            data, clientAddress = serverUdpSocket.recvfrom(dataLen)
            msg_type, seqNum = unpack("!ii", data)
            if drop < THRESHOLD:
                data = pack('!ii', 2, seqNum)
                serverUdpSocket.sendto(data, clientAddress)
            else:
                print("Message with sequence number%d from %s dropped" %(seqNum, clientAddress))


