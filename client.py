# Client
import socket
 

def Main():
    # local host IP '127.0.0.1'
    host = '127.0.0.1'
 
    # Define the port on which you want to connect
    port = 9000
 
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
 
    # connect to server on local computer
    s.connect((host,port))
 
    # message you send to server
    my_id = input("Enter client ID: ")
    while True:
       
        # Opening the binary file in binary mode as rb(read binary)
        f = open("godzy.jpg", mode="rb")
 
        # Reading file data with read() method
        data = f.read()
 
 
        # Closing the opened file
        f.close()
        # message sent to server
        s.send(data)
 
        # message received from server
        receved_data = s.recv(1024)
 
        # print the received message
        # here it would be a reverse of sent message
        print('Received from the server :',str(receved_data.decode('ascii')))
 
        # ask the client whether he wants to continue
        ans = input('\nDo you want to continue(y/n) :')
        if ans == 'yes':
            continue
        else:
            break
    # close the connection
    s.close()
 
if __name__ == '__main__':
    Main()
