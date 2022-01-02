from os import name
from shutil import Error
import socket
import sys
import struct as stru
import time as t
import threading
import random
from scapy.all import *

lock = threading.Lock()
done = False
has_winn = False
stop_broadcast = False
q = ["2+2", "3*3", "4-1", "6+2", "1+5", "8-4", "9-4"]
a = [4, 9, 3, 8, 6, 4, 5]


def send_invites(UDPSocket, data_to_send, port):
    global stop_broadcast
    Broadcast_address = ('<broadcast>', port)
    while (not stop_broadcast):
        # wait for a second
        t.sleep(1)
        # send the broadcast
        UDPSocket.sendto(data_to_send, Broadcast_address)


def get_answer(sock: socket, name1, name2, answer):
    global has_winn, done
    message = "Game over!\nThe correct answer was " + str(answer) + "!\n\nCongratulations to the winner: "
    sock.settimeout(10)
    try:
        data = sock.recv(1)
        ans = (data).decode()
        with lock:
            if (not done):
                done = True
                if (ans == answer):
                    message = str(message) + str(name1)
                    sock.sendall(message.encode())
                    has_winn = True
                else:
                    message = str(message) + str(name2)
                    sock.sendall(message.encode())
            elif not has_winn:
                message = str(message) + str(name1)
                sock.sendall(message.encode())
                has_winn = True
            elif has_winn:
                message = str(message) + str(name2)
                sock.sendall(message.encode())
        sock.close()
    except socket.timeout:
        if not done and not has_winn:
            sock.sendall(("Game over!\nThe correct answer was " + str(answer) + " .It was a draw.").encode())
        else:
            message = str(message) + str(name2)
            sock.sendall(message.encode())
        sock.close()


def SetGameSocket():
    TCPsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    TCPsock.bind(('', 2098))
    TCPsock.listen(2)
    return TCPsock


def setBroadcastSock():
    # Create a UDP socket
    UDPSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    UDPSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    UDPSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    UDPSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Bind the socket to the port
    UDPSocket.bind(('', 13117))
    return UDPSocket


def createMessage():
    return stru.pack('>IbH', 0Xabcddcba, 0X2, 2098)


# check in lab the broadcast ip
HOST = get_if_addr("eth2")
print("Server started, listening on IP address ", HOST)
msg = createMessage()
UDPSock = setBroadcastSock()

while True:
    TCPsock = SetGameSocket()
    stop_broadcast = False
    broadcaster = threading.Thread(target=send_invites, args=(UDPSock, msg, 13117))
    broadcaster.start()
    conn1, addr1 = TCPsock.accept()
    conn2, addr2 = TCPsock.accept()
    stop_broadcast = True
    broadcaster.join()
    print("Two participants connected. starting game in 10 seconds")
    t.sleep(3)
    name1 = conn1.recv(1024).decode()
    name2 = conn2.recv(1024).decode()
    if not name1:
        conn1.close()
        conn2.close()
        continue
    if not name2:
        conn1.close()
        conn2.close()
        continue
    name1 = name1[:-1]
    name2 = name2[:-1]
    loc = random.randint(0, 6)
    ques = q[loc]
    ans = a[loc]
    message = "\n\nWelcome to Quick Maths.\nPlayer 1: " + str(name1) + "\nPlayer2: " + str(
        name2) + "\nHow much is " + str(ques) + "?\n"
    conn1.sendall(message.encode())
    conn2.sendall(message.encode())
    receiver1 = threading.Thread(target=get_answer, args=(conn1, name1, name2, ans))
    receiver2 = threading.Thread(target=get_answer, args=(conn2, name2, name1, ans))
    receiver1.start()
    receiver2.start()
    receiver1.join()
    receiver2.join()
    conn1.close()
    conn2.close()
    TCPsock.close()
    t.wait(10)
    # update on starting a new game
    print("Game over, sending out offer requests...\n\n")

