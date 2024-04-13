# Client
import socket
import random
from common import *
import time

demo_write = ["aaaa", "bbb", "ccc","ddd", "eee", "fff", "ggg", "hhh", "iii"]

def get_rand_out_of_4_id():
    num = time_now() # number of seconds that passed since January 1, 1970, 00:00:00 UTC
    randomizer = random.randrange(1,4) 
    return num % randomizer

def send_to_server_both_ids(server_socket):
    # message from server with 2 different ids
    my_id = get_rand_out_of_4_id() 
    friend_id_to_request = get_rand_out_of_4_id()
    while (my_id == friend_id_to_request):
        friend_id_to_request = get_rand_out_of_4_id() # if the ids are the same, change the second id until both are different
    return str(my_id) + "," + str(friend_id_to_request) # send both ids to server



def Main():
    server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    # connect to server on local computer
    server_socket.connect((server_ip, server_port))
    server_msg = send_to_server_both_ids(server_socket)
     
    server_socket.send(rsa_encrypt_msg(server_msg))
    print("sent to server request to connect with msg : "+ server_msg)     
    
    response = str(rsa_decrypt_msg(server_socket.recv(256)))[2:-1]
    print("got response: ", response)
    if not response.startswith("please_start"):
        print("error")
        server_socket.close()
        return

    # now we start writing !
    for i in demo_write:
        random_variable = random.choice(demo_write)
        server_socket.send(rsa_encrypt_msg(random_variable))
        time.sleep(2)
        # TODO later support quit
    server_socket.close()
 
if __name__ == '__main__':
    Main()
''