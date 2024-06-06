import socket
import time
import select
import queue
import tkinter as tk
import common
import dbtools
import datetime
from _thread import *
import threading
from dbtools import *
from common import *
from project_gui import run_gui
from project_gui import update_textbox
from project_gui import display_message
from dbtools import Dbfunc
from login_gui import LoginGUI

encryptObj = Encryption()
dbTool = Dbfunc()
connections_map = {} # dictionary in order to keep track of the client's connections
current_date = datetime.now().date()

# Initialize mydb_db outside of initialize_db() function
mydb_db = None

# thread function for client
def threaded(client_socket, encryptObj):
    message_queue = queue.Queue()
    text_box = ""
    out_queue = queue.Queue() # we use queue in order to read the messages from ui
    gui_thread = threading.Thread (target=run_gui, args = (message_queue, out_queue, text_box)) # creates a new thread object that run the GUI
    gui_thread.start() # we launch the GUI
    msg = str(encryptObj.rsa_decrypt_msg(client_socket.recv(256)))[2:-1] # receive client's message
    message_queue.put("__"+ msg) # put the message in the queue
    (first_id, second_id )= msg.split(",") # splits the tupple in order to access the variables
    connections_map.update({first_id : client_socket}) # puts the first id as the key for the client socket, allows the server to keep track of each client's connection
    while(second_id not in connections_map.keys()): # while the connection between the clients is still unavailable we keep on waiting before proceeding
        event = threading.Event()
        event.wait(5)  # Wait for the second client to connect
    common.shared_vars["connection_status"] = True
    message_queue.put("now we have a connection")
    print("\n\n\nnow we have a connection", message_queue)
    client_socket.setblocking(False) # server starts receiving data from now on
    client_socket.settimeout(3)
    # TODO(version 2) - probably no need as we show all messages.. tbd later..smth like this: if client_socket > second_socket do nothing and if not - handle chat
    second_socket = connections_map[second_id] # add second id's connection as second socket to the dictionary
    print(connections_map)
    print ("__", first_id, second_id)
    client_socket.send(encryptObj.rsa_encrypt_msg("please_start")) # let the first client know that the connection has started

    print("_%%%%__", second_socket,)
    second_socket.send(encryptObj.rsa_encrypt_msg("please_start")) # let the second client know that the connection has started
    chat_sockets = [client_socket, second_socket] # chat's connections
    while True: # while the connection is available
        if not out_queue.empty(): # if there is still more
            # todo send-all
            ready_read, _, _ = select.select(chat_sockets, chat_sockets, [])
            for sock in ready_read:
                data = str(encryptObj.rsa_decrypt_msg(sock.recv(256)))[2:-1]
                print(data)
                if sock == client_socket:
                    other_sock = second_socket
                else:
                    other_sock = client_socket
                other_sock.send(encryptObj.rsa_encrypt_msg(data))
            # note that when change to UI should be shown only once for each couple
            message_queue.put(data)
    # data received from client
       
    # connection closed
    client_socket.close()
    connections_map.popitem(first_id) # removes the client connection from the dictionary when the chat ends




def initialize_db(): # the funtion that starts the database
    global mydb_db
    mydb = dbTool.init()
    dbTool.create_database("mysql") # creates database(mydb)
    dbs = dbTool.show_databases()    
    mydb_db = dbTool.init_with_db("mysql") # takes the variable as an argument for connection with "mysql" database
    return mydb_db # returns the argument that connects to the database




def create_tables(mydb_db): # create all of the tables
    dbTool.create_table(mydb_db, "mediapics",
                "(id VARCHAR(255), filesize INT, filename VARCHAR(255), clientids INT, datepublished DATE, sessionsid INT)")
    dbTool.create_table(mydb_db, "clients",
                "(id VARCHAR(255), full_name VARCHAR(255), ip VARCHAR(255), port VARCHAR(255), credibility INT, previous_sessions VARCHAR(255), client_ids_friends VARCHAR(255), text_ids INT, pics_ids INT )")
    dbTool.create_table(mydb_db, "mediavids",
                "(id VARCHAR(255), filesize INT, filename INT, length INT, path INT)")
    dbTool.create_table(mydb_db, "textmessages",
                "(id VARCHAR(255), clientidsent INT, clientidreceived INT, date DATE, isseen BOOL)")
    dbTool.create_table(mydb_db, "sessions",
                "(id VARCHAR(255), senderid INT, receivedid INT, objtype VARCHAR(255), objid INT, date DATE)")


class Server:
    def __init__(self):
        mydb_db = initialize_db() # creates a database and puts mydb_db as a connection argument for it
        create_tables(mydb_db) # creates the tables from the given database
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # socket(adress family of the socket and ip, connection type)
        s.bind((server_ip, server_port)) # binds the socket with the ip and the port in order to let the server recive connection from clients
        print("socket binded to port", server_port)
        s.listen(5) # put the socket into listening mode
        print("socket is listening")

        # a forever loop until client wants to exit
        while True:
            # establish connection with client
            c, addr = s.accept()
            print('Connected to :', addr[0], ':', addr[1])
            # Start a new thread and return its identifier
            start_new_thread(threaded, (c, encryptObj,))
        s.close()


if __name__ == '__main__':
    Server()