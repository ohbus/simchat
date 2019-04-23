import sys, socket, select

HOST = ''
SOCKET_LIST = []
RECV_BUFFER = 36361 
PORT = 36360

def chat_server():
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(10)

    uname = dict()
 
    # add server socket object to the list of readable connections
    SOCKET_LIST.append(server_socket)
 
    print ("Chat server started on port " + str(PORT))
 
    while 1:

        # get the list sockets which are ready to be read through select
        # 4th arg, time_out  = 0 : poll and never block
        try:
            read_sockets,write_sockets,error_sockets = select.select(SOCKET_LIST,[],[],0)
        except:
            sys.exit("\n")

        for sock in read_sockets:
            # a new connection request recieved
            if sock == server_socket: 
                sockfd, addr = server_socket.accept()
                SOCKET_LIST.append(sockfd)
                #print (sockfd, addr)
                print ("Client (%s, %s) connected" % addr)
                 
                broadcast(server_socket, sockfd, "[%s:%s] entered our chatting room\n" % addr)
             
            # a message from a client, not a new connection
            else:
                # process data recieved from client, 
                try:
                    # receiving data from the socket.
                    data = sock.recv(RECV_BUFFER).decode()
                    #print(sock.getpeername(), data)

                    if(sock.getpeername() not in uname):
                        uname[sock.getpeername()] = data
                        continue

                    if data:
                        # there is something in the socket
                        broadcast(server_socket, sock, "\r" + '<' + uname[sock.getpeername()] + '> ' + data)  
                    else:
                        # remove the socket that's broken    
                        if sock in SOCKET_LIST:
                            SOCKET_LIST.remove(sock)

                        # at this stage, no data means probably the connection has been broken
                        broadcast(server_socket, sock, "[*] %s is now offline\n" % uname[sock.getpeername()]) 
                        #broadcast(server_socket, sock, "Client (%s, %s) is offline\n" % addr) 

                # exception 
                except:
                    #broadcast(server_socket, sock, "Client (%s, %s) is offline\n" % addr)
                    broadcast(server_socket, sock, "[*] %s is now offline\n" % uname[sock.getpeername()])
                    continue

    server_socket.close()
    
# broadcast chat messages to all connected clients
def broadcast (server_socket, sock, message):
    for socket in SOCKET_LIST:
        # send the message only to peer
        if socket != server_socket and socket != sock :
            try :
                socket.send(message.encode())
            except :
                # broken socket connection
                socket.close()
                # broken socket, remove it
                if socket in SOCKET_LIST:
                    SOCKET_LIST.remove(socket)
 
if __name__ == "__main__":
    try:
        HOST = sys.argv[1]
    except:
        HOST = ''
    sys.exit(chat_server())
