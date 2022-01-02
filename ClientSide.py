from os import wait
import select as sel

import socket
import struct as str
import sys
from scapy.all import *


game_over=False
answers=0

def read(conn):
    global answers
    data = conn.recv(1024)
    if data:
        answers=answers+1
        print(data.decode())


def answer(conn):
    ans = sys.stdin.read(1)
    conn.sendall(ans.encode())

name = "Avengers\n"
# ip_type = input("Choose eth1 or eth2 =>\n")
HOST= get_if_addr("eth2")

def setUdpConn():
    UDPSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    UDPSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    UDPSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    UDPSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    UDPSocket.bind(('', 13117))
    return UDPSocket

def setTcpConn(ip,port):
    print("Received offer from server at" , ip , " , attempting to connect...")
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.connect((ip, port))
    tcp_socket.sendall(name.encode())
    return tcp_socket

def getOffers():
    UDPSock= setUdpConn()
    mes, add = UDPSock.recvfrom(7)
    magic_cockie, tp, tcp_port = str.unpack('>IbH',mes)
    while magic_cockie != 0Xabcddcba or tp != 0X2:
        mes, add = UDPSock.recvfrom(7)
        magic_cockie, tp, tcp_port = str.unpack('>IbH',mes)
    UDPSock.close()
    return mes,add


while True:
    game_over=False
    print("\n\nClient started, listening for offer requests...")
    msg,address= getOffers()
    magic_cockie, tp, tcp_port = str.unpack('>IbH',msg)
    if magic_cockie == 0Xabcddcba and tp == 0X2:
        with setTcpConn(address[0],tcp_port) as TCPConn:
           while answers<2:
                readers, _, _ = sel.select([TCPConn, sys.stdin], [], [])
                for key in readers:
                    if key is TCPConn:
                        read(TCPConn)
                    else:
                        answer(TCPConn)


