from os import name
import socket
import sys
import struct as str
import time as t
import _thread
import threading
import random
from scapy.arch import get_if_addr

lock=threading.Lock()

def send_invites(stop,UDPSocket,data_to_send,Broadcast_address):
    while(not stop):
        #wait for a second
        t.sleep(1)
        #send the broadcast
        print("server send")
        UDPSocket.sendto(data_to_send,Broadcast_address)

def get_answer(sock:socket,name1,name2,answer,done,has_winner):
    with sock:
        sock.timeout(10)
        try:
            ans=sock.recv(1024)
            message="Game over!\nThe correct answer was "+answer+"!\n\nCongratulations to the winner: "
            with lock:
                if( not done ):
                    done=True
                    if(ans==answer):
                        message=message+name1
                        sock.sendall(str.pack("s",message))
                        has_winner=True
                    else :
                        message=message+name2 
                        sock.sendall(str.pack("s",message))
                elif not has_winner:
                        message=message+name1
                        sock.sendall(str.pack("s",message)) 
                elif has_winner:
                        message=message+name2
                        sock.sendall(str.pack("s",message)) 
        except sock.timeout as e:
            sock.sendall(str.pack("s","Oops, the time to answer has left. \nBe faster next time!"))           

send_stop=False
if __name__ == '__main__':
    #check in lab the broadcast ip
    BroadCastIp = get_if_addr('eth2')

    port=13117
    # Create a UDP socket
    UDPSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    UDPSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    # Bind the socket to the port
    Broadcast_address = ('<broadcast>', port)
    address=(BroadCastIp, port)
    print("Server started, listening on IP address", BroadCastIp)
    magic_cookie = 0xabcddcba
    msg_type= 0x2
   
    data_to_send=str.pack("Ihh",magic_cookie,msg_type,port)
    q=["2+2","3*3","4-1","6+2","1+5","8-4","9-4"]
    a=[4,9,3,8,6,4,5]
    TCPsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    TCPsock.bind(address)
    TCPsock.listen(2)
    with TCPsock:
        while True:
            send_stop=False
            print("open threads")
            _thread.start_new_thread(send_invites,(send_stop,UDPSocket,data_to_send,Broadcast_address))
            print("here")
            conn1, addr1 = TCPsock.accept()
            print("here")
            conn2, addr2 = TCPsock.accept()
            send_stop=True
            t.sleep(10)
            name1=str.unpack("s" ,conn1.recv(1024))
            name2=str.unpack("s" ,conn2.recv(1024))
            if not name1:
                    conn1.close()
                    conn2.close()
                    continue
            if not name2:
                    conn1.close()
                    conn2.close()
                    continue
            name1= name1[0,name1.index('\n')]
            name2= name2[0,name2.index('\n')]
            loc= random.randint(0,6)
            message= "Welcome to Quick Maths.\nPlayer 1: "+name1+"\nPlayer2: "+name2+"\nHow much is "+q[loc]+"?\n"    
            conn1.sendall(str.pack("s",message)) 
            conn2.sendall(str.pack("s",message))
            done=False
            _thread.start_new_thread(get_answer,(conn1,name1,a[loc],done)) 
            _thread.start_new_thread(get_answer,(conn2,name2,a[loc],done))
            #update on starting a new game
            print("Game over, sending out offer requests...")

  