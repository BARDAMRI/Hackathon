import socket
import struct as str
import selectors
import sys


sel = selectors.DefaultSelector()
conn = None





def read(conn, msk):
    data = conn.recv(1024)
    if data:
        print (str.unpack("s", data)[0])
    else:
        conn.close()
    sel.register(sys.stdin, selectors.EVENT_READ, answer)

def answer (std_in,msk):
    ans = std_in.readline(1)
    conn.sendall(str.pack("s",ans))
    sel.register(conn, selectors.EVENT_READ, read)



name = "Avengers\n"
port = 13117
address = ("", port)
print("Client started, listening for offer requests...")
UDPSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

UDPSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
UDPSocket.bind(address)



if __name__ == '__main__':
    while True:
     
        msg, address = UDPSocket.recvfrom(1024) 
        
        print(str.unpack("Ihh", msg))
        magic_cockie, tp, server_port = str.unpack("Ihh", msg)
        print(server_port)
        conn = tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(address)
        print("here connect1")
        tcp_socket.bind((address[0],server_port))
        print("here connect")
        tcp_socket.sendall(str.pack("h", name.split()))
        print("here")
        sel.register(tcp_socket, selectors.EVENT_READ, read)
        sel.register(sys.stdin, selectors.EVENT_READ, answer)

        events = sel.select()
        for key, msk in events:
            call_back = key.data
            call_back(key.fileobj, msk)
