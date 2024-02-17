import tkinter as tk
import socket
import threading

def send_message():
    message = entry_field.get()
    if message:
        chat_log.config(state=tk.NORMAL)
        chat_log.see(tk.END)
        chat_log.insert(tk.END, "You: " + message + "\n")
        chat_log.config(state=tk.DISABLED)
        entry_field.delete(0, tk.END)
        send_to_server(message)

def send_to_server(message):
    try:
        client_socket.send(message.encode())
    except Exception as e:
        print("Error sending message to server:", e)

def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                chat_log.config(state=tk.NORMAL)
                chat_log.see(tk.END)
                chat_log.insert(tk.END, message)
                chat_log.config(state=tk.DISABLED)
        except Exception as e:
            print("Error receiving message from server:", e)
            break

def on_enter(event):
    send_message()

# Create the main window
root = tk.Tk()
root.title("Simple Chat")

# Create a frame for the chat log
chat_frame = tk.Frame(root)
chat_frame.pack(expand=True, fill=tk.BOTH)

# Add a scrollbar to the chat frame
scrollbar = tk.Scrollbar(chat_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Create a text widget for the chat log
chat_log = tk.Text(chat_frame, wrap=tk.WORD, yscrollcommand=scrollbar.set)
chat_log.pack(expand=True, fill=tk.BOTH)
chat_log.config(state=tk.DISABLED)  # Disable editing of chat log

# Link the scrollbar to the chat log
scrollbar.config(command=chat_log.yview)

# Create a frame for the message entry field and send button
entry_frame = tk.Frame(root)
entry_frame.pack(fill=tk.X)

# Create an entry field for typing messages
entry_field = tk.Entry(entry_frame)
entry_field.pack(side=tk.LEFT, expand=True, fill=tk.X)
entry_field.bind("<Return>", on_enter)  # Bind Enter key to send_message

# Create a button to send messages
send_button = tk.Button(entry_frame, text="Send", command=send_message)
send_button.pack(side=tk.RIGHT)

# Focus on entry field by default
entry_field.focus_set()

# Connect to the server
HOST = '127.0.0.1'  # Server IP address
PORT = 6789         # Server port
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# Start a thread to receive messages from the server
receive_thread = threading.Thread(target=receive_messages)
receive_thread.daemon = True
receive_thread.start()

# Run the main event loop
root.mainloop()
