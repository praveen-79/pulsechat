import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import os

from database import signup


def open_login():
    window.destroy()
    login_path = os.path.join(os.path.dirname(__file__), "login_gui.py")
    subprocess.Popen([sys.executable, login_path])


def create_account(event=None):
    username = username_entry.get().strip()
    password = password_entry.get().strip()

    if not username or not password:
        messagebox.showwarning("Warning", "Please enter both username and password!")
        return

    if len(username) < 3:
        messagebox.showwarning("Warning", "Username must be at least 3 characters!")
        return

    if signup(username, password):
        messagebox.showinfo("Success", f"Account '{username}' created successfully!\nPlease log in.")
        open_login()
    else:
        messagebox.showerror("Error", "Username already exists! Please choose another.")


window = tk.Tk()
window.title("PulseChat - Create Account")
window.geometry("420x380")
window.resizable(False, False)
window.configure(bg="#1e1e2e")

# Title Header
title = tk.Label(
    window,
    text="Create Account",
    font=("Segoe UI", 20, "bold"),
    bg="#1e1e2e",
    fg="#ffffff"
)
title.pack(pady=(28, 5))

subtitle = tk.Label(
    window,
    text="Register to start chatting with others",
    font=("Segoe UI", 10),
    bg="#1e1e2e",
    fg="#a6adc8"
)
subtitle.pack(pady=(0, 20))

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
username_entry.pack(pady=(4, 12), ipady=5, padx=45)
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
password_entry.pack(pady=(4, 18), ipady=5, padx=45)

# Press Enter to Sign Up
username_entry.bind("<Return>", create_account)
password_entry.bind("<Return>", create_account)

# Sign Up Button
signup_button = tk.Button(
    window,
    text="SIGN UP",
    font=("Segoe UI", 11, "bold"),
    bg="#a6e3a1",
    fg="#11111b",
    activebackground="#94e2d5",
    activeforeground="#11111b",
    relief="flat",
    cursor="hand2",
    width=28,
    command=create_account
)
signup_button.pack(ipady=6, padx=45)

# Switch to Log In
login_link = tk.Button(
    window,
    text="Already have an account? Log In",
    font=("Segoe UI", 9, "underline"),
    bg="#1e1e2e",
    fg="#89dceb",
    activebackground="#1e1e2e",
    activeforeground="#b4befe",
    bd=0,
    cursor="hand2",
    command=open_login
)
login_link.pack(pady=(16, 0))

window.mainloop()