# Client
import socket
import random
from common import *
def get_rand_out_of_4_id():
    num = time_now() 
    randomizer = random.randrange(1,4)
    return num%randomizer   # timestemp number % a number between 0-3
def send_to_server_both_ids(server_socket):
    # message from server with 2 difirent ids
    my_id = get_rand_out_of_4_id()
    friend_id_to_request = get_rand_out_of_4_id()
    while (my_id == friend_id_to_request):
        friend_id_to_request = get_rand_out_of_4_id()
    return str(my_id) + "," +str(friend_id_to_request)
def send_to_server_both_ids_new(server_socket):
    # read from file
    pass
    


def Main():
    server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    # connect to server on local computer
    server_socket.connect((server_ip, server_port))
    server_msg = send_to_server_both_ids(server_socket)
     
    server_socket.send(server_msg.encode("ascii"))
    print("sent to server request to connect with msg : "+ server_msg)     
    
    response = server_socket.recv(1024).decode('ascii')
    print("got response: ", response)
    if response is successful_connection:

        # TODO start messaging from file #?
        pass

    # TODO how do you finish?

    server_socket.close()
 
if __name__ == '__main__':
    Main()
