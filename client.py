import sys, socket, select
 
def client():
    if(len(sys.argv) < 3) :
        print( 'Usage : python3 client.py [hostname] [port]')
        print( 'Default : [hostname] = client, [port] = 36360')

    try:
        host = sys.argv[1]
    except:
        host = 'client'

    try:
        port = int(sys.argv[2])
    except:
        port = 36360
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10)
     
    try :
        s.connect((host, port))
    except :
        print ('Unable to connect')
        sys.exit()
     
    print ('Connected to remote host. You can start sending messages. Ctrl+C to Exit.')
    uname = input("Enter Your uname: ")
    sys.stdout.write('<%s> ' %uname); sys.stdout.flush()
    s.send(uname.encode()) 
    
    while 1:
        socket_list = [sys.stdin, s]
        try:
            read_sockets,write_sockets,error_sockets = select.select(socket_list , [], [])
        except:
            sys.exit("\n")

        for sock in read_sockets:            
            if sock == s:
                data = (sock.recv(36361))
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
