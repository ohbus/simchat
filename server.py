import sys, socket, select

HOST = ''
SOCKET_LIST = []
RECV_BUFFER = 36002 
PORT = 36001

def chat_server():
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(10)

    uname = dict()
 
    SOCKET_LIST.append(server_socket)
 
    print ("Chat server started on port " + str(PORT))
 
    while 1:
        try:
            read_sockets,write_sockets,error_sockets = select.select(SOCKET_LIST,[],[],0)
        except:
            sys.exit("\n")

        for sock in read_sockets:
            if sock == server_socket: 
                sockfd, addr = server_socket.accept()
                SOCKET_LIST.append(sockfd)
                print ("Client (%s, %s) connected" % addr)
                 
                broadcast(server_socket, sockfd, "[%s:%s] entered our chatting room\n" % addr)
             
            else:
                try:
                    data = sock.recv(RECV_BUFFER).decode()

                    if(sock.getpeername() not in uname):
                        uname[sock.getpeername()] = data
                        continue

                    if data:
                        broadcast(server_socket, sock, "\r" + '<' + uname[sock.getpeername()] + '> ' + data)  
                    else:   
                        if sock in SOCKET_LIST:
                            SOCKET_LIST.remove(sock)

                        broadcast(server_socket, sock, "[*] %s is now offline\n" % uname[sock.getpeername()])

                except:
                    broadcast(server_socket, sock, "[*] %s is now offline\n" % uname[sock.getpeername()])
                    continue

    server_socket.close()
    
def broadcast (server_socket, sock, message):
    for socket in SOCKET_LIST:
        if socket != server_socket and socket != sock :
            try :
                socket.send(message.encode())
            except :
                socket.close()
                if socket in SOCKET_LIST:
                    SOCKET_LIST.remove(socket)
 
if __name__ == "__main__":
    try:
        HOST = sys.argv[1]
    except:
        HOST = ''
    sys.exit(chat_server())
