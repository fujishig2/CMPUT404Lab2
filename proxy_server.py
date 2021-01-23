#!/usr/bin/env python3
import socket
import time

#define address & buffer size
HOST = ""
PORT = 8001
BUFFER_SIZE = 1024

#get host information
def get_remote_ip(host):
    print(f'Getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname( host )
    except socket.gaierror:
        print ('Hostname could not be resolved. Exiting')
        sys.exit()

    print (f'Ip address of {host} is {remote_ip}')
    return remote_ip

#send data to server
def send_data(serversocket, data):
    print("Sending data")    
    try:
        serversocket.sendall(data)
    except socket.error:
        print ('Send failed')
        sys.exit()
    print("Data sent successfully")

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    
        #QUESTION 3
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        #bind socket to address
        s.bind((HOST, PORT))
        #set to listening mode
        s.listen(2)
        
        #continuously listen for connections
        while True:
            conn, addr = s.accept()
            print("Connected by", addr)
            
            #recieve data, wait a bit, then send it back
            full_data = conn.recv(BUFFER_SIZE)
            time.sleep(0.5)
            
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as t:
                
                #define address info, payload, and buffer size
                host = 'www.google.com'
                port = 80
                buffer_size = 1024
                
                remote_ip = get_remote_ip(host)
        
                t.connect((remote_ip , port))
                print (f'Socket Connected to {host} on ip {remote_ip}')     
                
                #send the data and shutdown
                send_data(t, full_data)
                t.shutdown(socket.SHUT_WR)
        
                #continue accepting data until no more left
                google_data = b""
                while True:
                    data = t.recv(buffer_size)
                    if not data:
                         break
                    google_data += data
                print("Sending proxy data to client connected.")
                conn.sendall(google_data)
                conn.close()

if __name__ == "__main__":
    main()