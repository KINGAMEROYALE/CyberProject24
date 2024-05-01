import tkinter as tk
import threading
import queue
import time

root = ""
text_box = ""
entry_field = ""


# Function to update the textbox with new messages
def update_textbox(q):
    while True:
        if not q.empty():
            message = q.get()
            display_message(message)
        root.update_idletasks()
        time.sleep(0.1)

# Function to display a message in the textbox
def display_message(message):
    text_box.config(state=tk.NORMAL)
    text_box.insert(tk.END, "\n")
    text_box.insert(tk.END, message, "user_message")
    text_box.insert(tk.END, "\n")
    text_box.see(tk.END)
    text_box.config(state=tk.DISABLED)

# Function to send a message to the server
def send_message(entry_field):
    message = entry_field.get()
    if message.strip():  # Check if the message string is not empty after stripping whitespace
        print("Entry field value:", message)
        entry_field.delete(0, tk.END)  # Clear the entry field after sending the message
        
        return message  # Return the message
    else:
        print("Entry field is empty!")
        return ""


# Function to close the chat window
def close_chat():
    root.destroy()

# Function to run the GUI
def run_gui(message_queue):
    global root
    global text_box
    root = tk.Tk()
    root.title("Chat")

    # Textbox to display messages
    text_box = tk.Text(root, wrap=tk.WORD)
    text_box.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # Entry field for typing messages
    entry_field = tk.Entry(root)
    entry_field.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)  # Adjusted to fill both horizontally and vertically

    # Send button
    send_button = tk.Button(root, text="Send", command=lambda: send_message(entry_field)) # lamboda is the result of the funtion
    send_button.pack(side=tk.RIGHT, fill=tk.Y)  # Adjusted to fill vertically

    # Close button
    close_button = tk.Button(root, text="X", bg="red", command=close_chat)
    close_button.place(relx=1.0, rely=0.0, x=-5, y=5, anchor="ne")  # Position the "X" button at the top right corner

    # Add an empty line after the "X" button
    text_box.insert(tk.END, "\n")

    # Configure tag for user message
    text_box.tag_configure("user_message", justify="right", background="lightblue", relief=tk.RAISED, wrap=tk.WORD)

    # Thread to update the textbox
    update_thread = threading.Thread(target=update_textbox, args=(message_queue,), daemon=True)
    update_thread.start()

    root.mainloop()