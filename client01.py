import socket
import threading
import requests
import random
import json
import tkinter as tk
from tkinter import messagebox

def client_gui():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 5678)
    client_socket.connect(server_address)

    def send_answer():
        answer = answer_var.get()
        if answer.isdigit():
            client_socket.send(answer.encode('utf-8'))
            answer_var.set("")
        else:
            messagebox.showerror("Błąd", "Podaj numer odpowiedzi!")

    def receive_messages():
        while True:
            try:
                message = client_socket.recv(1024).decode('utf-8')
                if not message:
                    break
                output_text.config(state=tk.NORMAL)
                output_text.insert(tk.END, message + '\n')
                output_text.config(state=tk.DISABLED)
                output_text.see(tk.END)
            except ConnectionAbortedError:
                break

    root = tk.Tk()
    root.title("Quiz")

    output_text = tk.Text(root, height=15, width=50, state=tk.DISABLED)
    output_text.pack(pady=10)

    answer_var = tk.StringVar()
    answer_entry = tk.Entry(root, textvariable=answer_var)
    answer_entry.pack(pady=5)

    send_button = tk.Button(root, text="Wyślij odpowiedź", command=send_answer)
    send_button.pack(pady=5)

    threading.Thread(target=receive_messages, daemon=True).start()

    root.mainloop()

    client_socket.close()

if __name__ == "__main__":
    client_gui()