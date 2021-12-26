import socket
import struct as str

name="Avengers"
port=13117
BroadCastIp=''
address=(BroadCastIp,port)
print("Client started, listening for offer requests...")
UDPSocket= socket.socket(socket,socket.AF_INET,socket.SOCK_DGRAM)
UDPSocket.bind(port)
while True:
    connection,address= UDPSocket.accept()
    magic_cookie ,msg_type,server_port=str.unpack("!Ihh",connection.recv(1024))
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((address[0],server_port))
        s.sendall(str.pack("s",name+'\n'))
        print(str.unpack("s",s.recv(1024)))
        s.sendall(str.pack("s",input("Your answer: ")))
        print(str.unpack("s",s.recv(1024)))
    




