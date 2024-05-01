# Client
import socket
import random
from common import *
import time
import threading
from project_gui import send_message, entry_field



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




def receive_from_server(server_socket):
    while True:
        try:
            data = rsa_decrypt_msg(server_socket.recv(256)).decode("utf-8")
            if data:
                print("Received from server:", data)  # Print received message for debugging
                # Display received message in the GUI
                # For example:
                # display_message_in_gui(data)
        except Exception as e:
            print("Error receiving message from server:", e)
            break

def Main():
    server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)


    # connect to server on local computer
    server_socket.connect((server_ip, server_port)) # connect socket to server ip and port
    server_msg = send_to_server_both_ids(server_socket) # send two client's ids to the server    
    server_socket.send(rsa_encrypt_msg(server_msg)) # sends the two ids in an encrypted message
    print("sent to server request to connect with msg : "+ server_msg)
   
    response = str(rsa_decrypt_msg(server_socket.recv(256)))[2:-1]
    print("got response: ", response)
    if response is None or response == "":
        print("error")
        server_socket.close()
        return
    if not response.startswith("please_start"):
        print("error") # ?
        server_socket.close()
        return

    receive_thread = threading.Thread(target=receive_from_server, args=(server_socket,))
    receive_thread.start()

    time.sleep(3)
    # now we start writing !
    for message in demo_write:
        entry = send_message(entry_field)  # Store the return value of send_message
        print("Random variable:", entry)  # Print the value for debugging
        server_socket.send(rsa_encrypt_msg(entry))  # Send the message to the server
        time.sleep(8)
    server_socket.close()
 
if __name__ == '__main__':
    Main()
''
