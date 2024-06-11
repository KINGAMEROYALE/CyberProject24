import socket
import threading
import queue
from project_gui import run_gui
import common
from tkinter import Tk, Label, Entry, Button
from common import Encryption

encryptObj = Encryption()

class Client:
    def __init__(self):
        self.server_socket = None
        self.message_queue = queue.Queue()
        self.my_id = None
        self.friend_id = None

    def connect_to_server(self, my_id, friend_id):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.connect((common.server_ip, common.server_port))

        server_msg = f"{my_id},{friend_id}"
        self.server_socket.send(encryptObj.rsa_encrypt_msg(server_msg))
        print("Sent to server request to connect with msg: " + server_msg)

        response = str(encryptObj.rsa_decrypt_msg(self.server_socket.recv(256)))[2:-1]
        print("Got response: ", response)
        if response == "now we have a connection":
            common.shared_vars["connection_status"] = True
            receive_thread = threading.Thread(target=self.receive_from_server)
            receive_thread.start()
            run_gui(self.message_queue, self.server_socket)
        else:
            print("Error: Unexpected response from server")
            self.server_socket.close()

    def receive_from_server(self):
        while True:
            try:
                data = encryptObj.rsa_decrypt_msg(self.server_socket.recv(256)).decode("utf-8")
                if data:
                    print("Received from server:", data)
                    self.message_queue.put(data)
                    print("received")
            except Exception as e:
                print("Error receiving message from server:", e)
                break

def show_login_window():
    def on_submit():
        my_id = client_id_entry.get()
        friend_id = friend_id_entry.get()
        if my_id and friend_id:
            login_root.destroy()
            client.connect_to_server(my_id, friend_id)

    login_root = Tk()
    login_root.title("Login")

    Label(login_root, text="Client ID").grid(row=0, column=0)
    client_id_entry = Entry(login_root)
    client_id_entry.grid(row=0, column=1)

    Label(login_root, text="Friend ID").grid(row=1, column=0)
    friend_id_entry = Entry(login_root)
    friend_id_entry.grid(row=1, column=1)

    submit_button = Button(login_root, text="Submit", command=on_submit)
    submit_button.grid(row=2, columnspan=2)

    login_root.mainloop()

if __name__ == '__main__':
    client = Client()
    show_login_window()
