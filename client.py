import socket
import random
from common import *
import time
import threading
import os
import base64
import queue
from project_gui import send_message

encryptObj = Encryption()
timenow = Time()


demo_write = ["aaaa", "bbb", "ccc","ddd", "eee", "fff", "ggg", "hhh", "iii"]

def get_client_id():
    return int(input("Please enter your client ID: "))

def get_friend_id():
    return int(input("Please enter the client ID you want to connect with: "))

def send_to_server_both_ids(server_socket):
    # message from server with 2 different ids
    my_id = get_client_id()
    friend_id_to_request = get_friend_id()
    while (my_id == friend_id_to_request):
        time.wait(0.1)
    return str(my_id) + "," + str(friend_id_to_request) # send both ids to server


class Client:
    
    def __init__(self):
        server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

        # connect to server on local computer
        server_socket.connect((server_ip, server_port)) # connect socket to server ip and port
        server_msg = send_to_server_both_ids(server_socket) # send two client's ids to the server    
        server_socket.send(encryptObj.rsa_encrypt_msg(server_msg)) # sends the two ids in an encrypted message
        print("sent to server request to connect with msg : "+ server_msg)
    
        response = str(encryptObj.rsa_decrypt_msg(server_socket.recv(256)))[2:-1] # client's request to connect to the server
        print("Got response: ", response)
        if response is None or response == "":
            print("error")
            server_socket.close()
            return
        if not response.startswith("please_start"):
            print("error") # ?
            server_socket.close()
            return

        self.message_queue = queue.Queue()  # Create a message queue
        receive_thread = threading.Thread(target=self.receive_from_server, args=(server_socket,))  # Pass the server_socket to receive_from_server
        receive_thread.start()


    def receive_from_server(self, server_socket):
        while True:
            try:
                data = encryptObj.rsa_decrypt_msg(server_socket.recv(256)).decode("utf-8")
                if data:
                    print("Received from server:", data)
                    self.message_queue.put(data)  # Put received data into the message queue
            except Exception as e:
                print("Error receiving message from server:", e)
                break


if __name__ == '__main__':
    Client()