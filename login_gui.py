import tkinter as tk

class LoginGUI:
    def __init__(self, login_callback):
        self.login_callback = login_callback

        self.root = tk.Tk()
        self.root.title("Login")

        self.client_id_label = tk.Label(self.root, text="Client ID:")
        self.client_id_label.grid(row=0, column=0, padx=10, pady=5)
        self.client_id_entry = tk.Entry(self.root)
        self.client_id_entry.grid(row=0, column=1, padx=10, pady=5)

        self.friend_id_label = tk.Label(self.root, text="Friend ID:")
        self.friend_id_label.grid(row=1, column=0, padx=10, pady=5)
        self.friend_id_entry = tk.Entry(self.root)
        self.friend_id_entry.grid(row=1, column=1, padx=10, pady=5)

        self.login_button = tk.Button(self.root, text="Login", command=self.login)
        self.login_button.grid(row=2, columnspan=2, padx=10, pady=10)

        self.root.mainloop()

    def login(self):
        client_id = self.client_id_entry.get()
        friend_id = self.friend_id_entry.get()
        self.login_callback(client_id, friend_id)
        self.root.destroy()
