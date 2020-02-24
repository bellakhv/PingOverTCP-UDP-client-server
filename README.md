# PingOverTCP-UDP-client-server

This scripts allow to sent "ping" request and reply over TCP/UDP as chosen by client.

PingClient.py [-h] -p PORT -n {tcp,udp} -i IP [-c COUNT] [-l LENGTH] [-t TIMEOUT]

optional arguments:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  Network port (eg. 23, 80, 161, ...)
  -n {tcp,udp}, --protocol {tcp,udp} Network protocol (tcp or udp)
  -i IP, --ip IP        IP or hostname of the server
  -c COUNT, --count COUNT Reply counts
  -l LENGTH, --length LENGTH Packet data length
  -t TIMEOUT, --timeout TIMEOUT Replay max timout (sec)

For testing mode (randomly droped packets) change to TEST=1
