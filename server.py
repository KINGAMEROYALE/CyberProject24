# Server
import socket
 
# import thread module
from _thread import *
import threading
from dbtools import *
print_lock = threading.Lock()
 
# thread function
def threaded(c):
    while True:
 
        # data received from client
        data = c.recv(102400)
       
        with open("godzy.jpg", "wb") as file:
            file.write(data)
            file.close()
 
        # reverse the given string from client
        data = "yey!!"
 
        # send back reversed string to client
        c.send(data.encode("ascii"))
 
    # connection closed

    c.close()

'''
import mysql.connector
def show_database():
   
    mydb = mysql.connector.connect(
     host="localhost",
     user="root",
     password="nir123"
)

    mycursor = mydb.cursor()

    mycursor.execute("SHOW DATABASES")

    for x in mycursor:
        print(x)
       
def show_tables():
   
    mydb = mysql.connector.connect(
     host="localhost",
     user="root",
     database="mysql",
     password="nir123"
)

    mycursor = mydb.cursor()

    mycursor.execute("SHOW TABLES")

    for x in mycursor:
        print(x)

def create_table():

    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="nir123",
    database = "mysql")
    mycursor = mydb.cursor()

    print("____3____")
    mycursor.execute("CREATE TABLE customers3 (name VARCHAR(255), address VARCHAR(255))")
'''
def initialize_db(host):
	mydb = init()
	print("____2____")
	create_database(mydb, "mysql")
	print("____3____")
	dbs = show_databases(mydb)    
	print(dbs)
	print("____4____")
	mydb_db = init_with_db("mysql")
	return mydb_db


def Main():
	host = '127.0.0.1'
	mydb_db = initialize_db(host)  

	print("_5_")
	tables = show_tables(mydb_db)
	print(tables)
	print("_5_")
	create_table(mydb_db, "mediapics",
	            "(id INT, filesize INT, filename VARCHAR(255), clientids INT, datepublished DATE, sessionsid INT)")
	create_table(mydb_db, "clients",
	            "(id INT, full_name VARCHAR(255), ip INT, port VARCHAR(255), credibility INT, previous_sessions VARCHAR(255), client_ids_friends VARCHAR(255), text_ids INT, pics_ids INT )")
	create_table(mydb_db, "mediavids",
	            "(id INT, filesize INT, filename INT, length INT, path INT)")
	create_table(mydb_db, "textmessages",
	            "(id INT, clientidsent INT, clientidrecieved INT, date DATE, isseen BOOL)")
	create_table(mydb_db, "sessions",
                "(id INT, senderid INT, recivedid INT, objtype VARCHAR(255), objid INT, date DATE)")
	print("_6_")
	tables = show_tables(mydb_db)
	print(tables)
	print("_7_")
	print(get_all_rows(mydb_db, "clients"))
	print("_8_")
	insert_row(mydb_db, "clients",
	                "(id, full_name, ip ,port ,credibility, previous_sessions, client_ids_friends, text_ids, pics_ids)",
	                "(%s, %s, %s, %s, %s, %s, %s, %s, %s)",
	                (1, "WIZI", 90 ,9000 ,100, 6, "ido", 7, 4))
	insert_row(mydb_db, "clients",
	                "(id, full_name, ip ,port ,credibility, previous_sessions, client_ids_friends, text_ids, pics_ids)",
	                "(%s, %s, %s, %s, %s, %s, %s, %s, %s)",
	                (2, "WIZKALAH", 70 ,9000 ,168,8, "idit", 8, 9))
	print("_9_")
	print(get_all_rows(mydb_db, "clients"))
	print("____10____")
	print("_11_")
	print(get_all_rows(mydb_db, "clients"))
   
	print("_12___")
	print(get_rows_from_table_with_value(mydb_db, "clients", "id", "1"))
   
	'''

   
   
   
	'''
	print("_4_")
	my_tables = show_tables(mydb_db)
	for i in my_tables:
		print(i)
	#if "seekers" not in my_tables:
	#	create_table("seekers")

	# reserve a port on your computer
	# in our case it is 12345 but it
	# can be anything
        
        
	port = 9000
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((host, port))
	print("socket binded to port", port)

	# put the socket into listening mode
	s.listen(5)
	print("socket is listening")

	# a forever loop until client wants to exit
	while True:

		# establish connection with client
		c, addr = s.accept()

		# lock acquired by client
		print_lock.acquire()
		print('Connected to :', addr[0], ':', addr[1])

		# Start a new thread and return its identifier
		start_new_thread(threaded, (c,))
	s.close()
 
 
if __name__ == '__main__':
    Main()