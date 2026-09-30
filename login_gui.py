import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import os

from database import login


def open_signup():
    window.destroy()
    signup_path = os.path.join(os.path.dirname(__file__), "signup_gui.py")
    subprocess.Popen([sys.executable, signup_path])


def check_login(event=None):
    username = username_entry.get().strip()
    password = password_entry.get().strip()
    host = host_entry.get().strip() or "127.0.0.1"

    if not username or not password:
        messagebox.showwarning("Warning", "Please enter both username and password!")
        return

    if login(username, password):
        window.destroy()
        import chat_client
        chat_client.start_chat(username, host=host)
    else:
        messagebox.showerror("Error", "Invalid username or password!")


window = tk.Tk()
window.title("PulseChat - Login")
window.geometry("420x430")
window.resizable(False, False)
window.configure(bg="#1e1e2e")

# Title Header
title_label = tk.Label(
    window,
    text="Welcome Back",
    font=("Segoe UI", 20, "bold"),
    bg="#1e1e2e",
    fg="#ffffff"
)
title_label.pack(pady=(24, 4))

subtitle_label = tk.Label(
    window,
    text="Sign in to join real-time chatrooms",
    font=("Segoe UI", 10),
    bg="#1e1e2e",
    fg="#a6adc8"
)
subtitle_label.pack(pady=(0, 16))

# Username Field
username_label = tk.Label(
    window,
    text="Username",
    font=("Segoe UI", 10, "bold"),
    bg="#1e1e2e",
    fg="#cdd6f4"
)
username_label.pack(anchor="w", padx=45)

username_entry = tk.Entry(
    window,
    font=("Segoe UI", 11),
    bg="#313244",
    fg="#ffffff",
    insertbackground="#ffffff",
    relief="flat",
    width=32
)
username_entry.pack(pady=(3, 10), ipady=4, padx=45)
username_entry.focus()

# Password Field
password_label = tk.Label(
    window,
    text="Password",
    font=("Segoe UI", 10, "bold"),
    bg="#1e1e2e",
    fg="#cdd6f4"
)
password_label.pack(anchor="w", padx=45)

password_entry = tk.Entry(
    window,
    show="*",
    font=("Segoe UI", 11),
    bg="#313244",
    fg="#ffffff",
    insertbackground="#ffffff",
    relief="flat",
    width=32
)
password_entry.pack(pady=(3, 10), ipady=4, padx=45)

# Server IP Field
host_label = tk.Label(
    window,
    text="Server IP (Default: 127.0.0.1)",
    font=("Segoe UI", 9),
    bg="#1e1e2e",
    fg="#a6adc8"
)
host_label.pack(anchor="w", padx=45)

host_entry = tk.Entry(
    window,
    font=("Segoe UI", 10),
    bg="#313244",
    fg="#ffffff",
    insertbackground="#ffffff",
    relief="flat",
    width=32
)
host_entry.insert(0, "127.0.0.1")
host_entry.pack(pady=(3, 16), ipady=4, padx=45)

# Press Enter to Login
username_entry.bind("<Return>", check_login)
password_entry.bind("<Return>", check_login)
host_entry.bind("<Return>", check_login)

# Login Button
login_button = tk.Button(
    window,
    text="LOG IN",
    font=("Segoe UI", 11, "bold"),
    bg="#89b4fa",
    fg="#11111b",
    activebackground="#b4befe",
    activeforeground="#11111b",
    relief="flat",
    cursor="hand2",
    width=28,
    command=check_login
)
login_button.pack(ipady=6, padx=45)

# Switch to Sign Up
signup_link = tk.Button(
    window,
    text="Don't have an account? Sign Up",
    font=("Segoe UI", 9, "underline"),
    bg="#1e1e2e",
    fg="#89dceb",
    activebackground="#1e1e2e",
    activeforeground="#b4befe",
    bd=0,
    cursor="hand2",
    command=open_signup
)
signup_link.pack(pady=(14, 0))

window.mainloop()