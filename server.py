# Server
import socket
import time
import select
import queue
import tkinter as tk

# import thread module
from _thread import *
import threading
from dbtools import *
from common import *
from project_gui import *

connections_map = {}


# thread function for client

def threaded(client_socket, mydb_db):

		# ask for client ID
		#c.send(get_client_id_msg.encode("ascii"))
		# check in clients table if exists
		msg =client_socket.recv(1024).decode("ascii")
		print("____", msg)
		(first_id, second_id )= msg.split(",") 
		connections_map.update({first_id : client_socket})
		while(second_id not in connections_map.keys()):
			time.sleep(5) # pause for 5 seconds

		'''# no such user
		if not len(get_rows_from_table_with_value(mydb_db, "clients", "id", id)) :
			# create new user in db
			print("creating new user with id ", id)
			create_new_user_in_db(c, mydb_db)
		'''
		print("now we have a connection")
		
		client_socket.setblocking(False) 
		client_socket.settimeout(3)
		# TODO - probably no need as we show all messages.. tbd later..smth like this: if client_socket > second_socket do nothing and if not - handle chat
		second_socket = connections_map[second_id]
		chat_sockets = [client_socket, second_socket]
		while(True):
			ready_read, _, _ = select.select(chat_sockets, chat_sockets, [])
			for sock in ready_read:
				data = sock.recv(1024).decode("ascii")
				if sock == client_socket:
					other_sock = second_id
				else:
					other_sock = client_socket
				other_sock.send(data.encode("ascii"))
				# note that when change to UI should be shown only once for each couple
				print (data)

        # data received from client
        
       
    # connection closed
		client_socket.close()
		connections_map.popitem(first_id)

def initialize_db():
	mydb = init()
	create_database(mydb, "mysql")
	dbs = show_databases(mydb)    
	mydb_db = init_with_db("mysql")
	return mydb_db


def create_tables(mydb_db): 
	create_table(mydb_db, "mediapics",
	            "(id VARCHAR(255), filesize INT, filename VARCHAR(255), clientids INT, datepublished DATE, sessionsid INT)")
	create_table(mydb_db, "clients",
	            "(id VARCHAR(255), full_name VARCHAR(255), ip VARCHAR(255), port VARCHAR(255), credibility INT, previous_sessions VARCHAR(255), client_ids_friends VARCHAR(255), text_ids INT, pics_ids INT )")
	create_table(mydb_db, "mediavids",
	            "(id VARCHAR(255), filesize INT, filename INT, length INT, path INT)")
	create_table(mydb_db, "textmessages",
	            "(id VARCHAR(255), clientidsent INT, clientidrecieved INT, date DATE, isseen BOOL)")
	create_table(mydb_db, "sessions",
                "(id VARCHAR(255), senderid INT, recivedid INT, objtype VARCHAR(255), objid INT, date DATE)")
	tables = show_tables(mydb_db)


def Main():
	mydb_db = initialize_db()  
	create_tables(mydb_db)
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((server_ip, server_port))
	print("socket binded to port", server_port)

	# put the socket into listening mode
	s.listen(5)
	print("socket is listening")

	# Start GUI in a separate thread
	global message_queue
	message_queue = queue.Queue()
	gui_thread = threading.Thread (target=run_gui, args = (message_queue,))
	gui_thread.start()

	# a forever loop until client wants to exit
	while True:

		# establish connection with client
		c, addr = s.accept()

		print('Connected to :', addr[0], ':', addr[1])
		message_queue.put('Connected to '+ addr[0], ':' + str(addr [1]))
		# Start a new thread and return its identifier
		start_new_thread(threaded, (c,mydb_db,))
	s.close()


if __name__ == '__main__':
    Main()