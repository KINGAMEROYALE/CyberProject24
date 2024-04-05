import tkinter as tk
import threading
import queue
import time

def update_textbox(q):
    while True:
        if not q.empty():
            message = q.get()
            text_box.insert(tk.END, "\n" + message)
            text_box.see(tk.END)  # Scroll to the end
        root.update_idletasks()
        time.sleep(0.1)
        

def run_gui(message_queue):
    global root
    root = tk.Tk()
    root.title("Non-blocking Text Box Example")

    global text_box
    text_box = tk.Text(root)
    text_box.pack(fill=tk.BOTH, expand=True)



    # Create a thread for updating the text box
    update_thread = threading.Thread(target=update_textbox, args = (message_queue,), daemon=True)
    update_thread.start()


    root.mainloop()