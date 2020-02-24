# !/usr/local/bin/python2.7

'''
This script creates TCP/UDP connection to a server and send "ping" requests over it,
if the server is running it will reply to the client request.
'''

from time import time
from socket import *
from struct import *
import argparse
from utils import Connection

RTT = []  # this will store all time for each ping request in array format

def main():
    seqNum = 0
    packetsRecv = 0

    connectionInfo = setConnectionInfo()
    clientSocket = startConenection(connectionInfo)

    print("Pinging %s with %d byte of data" % (connectionInfo.hostname, connectionInfo.packetSize))

    while (seqNum < connectionInfo.count):
        start_time = time()
        seqNum += 1
        data = pack('!ii', 1, seqNum)  # packing sequence using struct big endian format
        clientSocket.sendto(data, (connectionInfo.hostname, connectionInfo.port))
        try:
            dataEcho, address = clientSocket.recvfrom(connectionInfo.packetSize)
            time_taken = (time() - start_time)*1000
            RTT.append(time_taken)
            msg_type, seq_rcv = unpack("!ii", dataEcho)
            print ("Reply from %s bytes=%d time=%sms" % (connectionInfo.hostname, connectionInfo.packetSize, time_taken))
            packetsRecv += 1  # increment successful packets received
        except Exception:
            print ("Ping message number %d got timed out" % (seqNum))

    if (connectionInfo.protocol == "tcp"):
        data = pack('!ii', 1, 0)  # end message for closing the tcp connection with zero seq
        clientSocket.sendto(data, (connectionInfo.hostname, connectionInfo.port))
    clientSocket.close()
    calcStatistics(connectionInfo, packetsRecv)


def setConnectionInfo():
    parser = argparse.ArgumentParser(description='Ping over TCP/UDP network client')
    parser.add_argument('-p', '--port' , action="store", type=int, required=True, help="Network port (eg. 23, 80, 161, ...)")
    parser.add_argument('-n', '--protocol' , action="store", choices=['tcp', 'udp'], required=True, help="Network protocol (tcp or udp)")
    parser.add_argument('-i', '--ip' , action="store", required=True, help="IP or hostname of the server")
    parser.add_argument('-c', '--count' , action="store", type=int, help="Reply counts", default=4)
    parser.add_argument('-l', '--length' , action="store", type=int, help="Packet data length ", default=32)
    parser.add_argument('-t', '--timeout' , action="store", type=int, help="Replay max timout (sec) ", default=1)
    args=parser.parse_args()
    port = args.port
    if (not(port >= 0 and port <= 65535)):
        sys.exit("Invalid port rage %s" % port)
    protocol = args.protocol
    timeout = args.timeout
    count = args.count
    ip = args.ip
    packetSize = args.length
    connectionInfo = Connection(ip, port, protocol, timeout, packetSize, count)
    return connectionInfo


def startConenection(connectionInfo):
    if connectionInfo.protocol.lower() == "tcp":
        try:
            clientSocket = socket(AF_INET, SOCK_STREAM)
        except socket.error:
            print "Failed to create TCP socket"
            sys.exit(1)
        serverInfo = (connectionInfo.hostname, connectionInfo.port)
        clientSocket.connect(serverInfo)
    elif connectionInfo.protocol.lower() == "udp":
        try:
            clientSocket = socket(AF_INET, SOCK_DGRAM)
        except socket.error:
            print "Failed to create UDP socket"
            sys.exit(1)
    else:
        sys.exit("Invalid protocol %s, exiting..." %connectionInfo.protocol)
    clientSocket.settimeout(connectionInfo.timeout)
    return clientSocket


def calcStatistics(connectionInfo, packetsRecv):
    packetsLost = connectionInfo.count - packetsRecv
    lostPercent = int(((float(packetsLost) / connectionInfo.count) * 100))

    print("Ping statistics for %s:" % (connectionInfo.hostname))
    print("Packets: Sent=%d, Received=%d, Lost=%d (%d%% Loss)" % (connectionInfo.count, packetsRecv, packetsLost, lostPercent))

    print("The Minimum RTT is: %.6f ms" % (min(RTT)))
    print("The Maximum RTT is: %.6f ms" % (max(RTT)))
    if packetsRecv != 0:
        print("The Average RTT is: %.6f ms" % ((sum(RTT) / packetsRecv)))
    else:
        print("The Average RTT is: 0ms")


if __name__ == "__main__":
    main()
