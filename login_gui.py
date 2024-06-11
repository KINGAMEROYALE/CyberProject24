import tkinter as tk

class LoginGUI:
    def __init__(self, master, on_submit):
        self.master = master
        self.master.title("Login")
        self.on_submit = on_submit

        self.client_id_label = tk.Label(master, text="Client ID")
        self.client_id_label.pack()

        self.client_id_entry = tk.Entry(master)
        self.client_id_entry.pack()

        self.friend_id_label = tk.Label(master, text="Friend ID")
        self.friend_id_label.pack()

        self.friend_id_entry = tk.Entry(master)
        self.friend_id_entry.pack()

        self.submit_button = tk.Button(master, text="Submit", command=self.submit)
        self.submit_button.pack()

    def submit(self):
        client_id = self.client_id_entry.get()
        friend_id = self.friend_id_entry.get()
        self.master.destroy()
        self.on_submit(client_id, friend_id)
