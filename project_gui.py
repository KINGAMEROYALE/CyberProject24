from PIL import Image, ImageTk
from tkinter import filedialog
import tkinter as tk
import threading
import queue
import time  # Import the time module for sleep
import socket
import common
from common import Encryption

root = ""
encryptObj = Encryption()

# Function to update the textbox with new messages
def update_textbox(q, text_box):
    while True:
        if not q.empty():
            print("------getting____", q)
            message = q.get()
            display_message(message, text_box)
        root.update_idletasks()
        time.sleep(0.1)  # Use the time module for sleeping

# Function to display a message in the textbox
def display_message(message, text_box):
    text_box.config(state=tk.NORMAL)
    text_box.insert(tk.END, "\n")
    text_box.insert(tk.END, message, "user_message")
    text_box.insert(tk.END, "\n")
    text_box.see(tk.END)
    text_box.config(state=tk.DISABLED)

def display_image(image_path, text_box):
    image = Image.open(image_path)
    image = image.resize((300, 300), Image.ANTIALIAS)  # Adjust the size as needed
    photo = ImageTk.PhotoImage(image)
    text_box.image = photo  # Store the photo as an attribute of the text box widget
    text_box.image_create(tk.END, image=photo)  # Insert the image into the text box at the end
    text_box.insert(tk.END, "\n")  # Insert a newline after the image
    text_box.see(tk.END)  # Scroll to the end of the text box

# Function to send a message to the server
def send_message(entry_field, message_queue, text_box, client_socket):
    print("inside send message")
    message = entry_field.get()
    if common.shared_vars["connection_status"]:
        if message.strip():
            print("Entry field value:", message)
            message_queue.put(message)  # Put the message directly into the message queue
            display_message(message, text_box)  # Display the message in the sender's GUI
            client_socket.send(encryptObj.rsa_encrypt_msg(message))  # Send the message to the server
            entry_field.delete(0, tk.END)  # Clear the entry field after sending the message
        else:
            print("Entry field is empty!")
    else:
        print("There is no connection between the clients yet.")


def select_media(text_box):
    # Ask the user to select a file
    global file_path
    file_path = filedialog.askopenfilename()
    display_image(file_path, text_box)

# Function to close the chat window
def close_chat():
    root.destroy()

# Function to run the GUI
def run_gui(message_queue, client_socket):
    print("inside run gui")
    global root
    root = tk.Tk()
    root.title("Chat")

    # Textbox to display messages
    text_box = tk.Text(root, wrap=tk.WORD)
    text_box.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # Entry field for typing messages
    entry_field = tk.Entry(root)
    entry_field.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)  # Adjusted to fill both horizontally and vertically
    
    # Send button
    send_button = tk.Button(root, text="Send", command=lambda: send_message(entry_field, message_queue, text_box, client_socket))
    send_button.pack(side=tk.RIGHT, fill=tk.Y)  # Adjusted to fill vertically
    
    plus_button = tk.Button(root, text="+", command=lambda: select_media(text_box))  # Add functionality here
    plus_button.pack(side=tk.LEFT, fill=tk.Y)  # Adjusted to fill vertically

    # Close button
    close_button = tk.Button(root, text="X", bg="red", command=close_chat)
    close_button.place(relx=1.0, rely=0.0, x=-5, y=5, anchor="ne")  # Position the "X" button at the top right corner

    # Add an empty line after the "X" button
    text_box.insert(tk.END, "\n")

    # Configure tag for user message
    text_box.tag_configure("user_message", justify="right", background="lightblue", relief=tk.RAISED, wrap=tk.WORD)

    # Thread to update the textbox
    update_thread = threading.Thread(target=update_textbox, args=(message_queue, text_box,), daemon=True)
    update_thread.start()

    root.mainloop()

