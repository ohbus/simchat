import sys, socket, select
 
def client():
    if(len(sys.argv) < 3) :
        print( 'How to use : python client.py [hostname] [port]')
        print( 'hostname is the name of the server machine or you can also provide the IP address as well.')
        print( 'Default : [hostname] = localhost , [port] = 36001')

    try:
        host = sys.argv[1]
    except:
        host = 'localhost'

    try:
        port = int(sys.argv[2])
    except:
        port = 36001
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10)
     
    try :
        s.connect((host, port))
    except :
        print ('Unable to connect to the server\nTable number 26 pe jaayiye. xD')
        sys.exit()
     
    print ('Connected to remote host. You can start sending messages. Ctrl+C to Exit.')

    uname = input("Enter Your USERNAME: ")

    sys.stdout.write('<%s> ' %uname); 
    sys.stdout.flush()
    s.send(uname.encode()) 
    
    while 1:
        socket_list = [sys.stdin, s]
        try:
            read_sockets,write_sockets,error_sockets = select.select(socket_list , [], [])
        except:
            sys.exit("\n")

        for sock in read_sockets:            
            if sock == s:
                data = (sock.recv(36002))
                data = data.decode()
                if not data :
                    print('\nDisconnected from chat server')
                    sys.exit()
                else :
                    sys.stdout.write(data)
                    sys.stdout.write('<%s> ' %uname); sys.stdout.flush()     
            
            else :
                msg = sys.stdin.readline().encode()
                s.send(msg)
                sys.stdout.write('<%s> ' %uname); sys.stdout.flush() 

if __name__ == "__main__":
    sys.exit(client())
