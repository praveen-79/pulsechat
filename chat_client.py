import tkinter as tk
from tkinter import simpledialog, messagebox
import socket
import threading
import sys

HOST = "127.0.0.1"
PORT = 5555
PUBLIC_TARGET = "📢 [Everyone (Public)]"


def start_chat(username, host=HOST):
    # -----------------------------
    # Connect to Server
    # -----------------------------
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((host, PORT))
        client.sendall((username + "\n").encode())
    except Exception as e:
        messagebox.showerror(
            "Connection Error",
            f"Could not connect to chat server at {host}:{PORT}.\n\n"
            "Please ensure server.py is running, then try again."
        )
        return

    # -----------------------------
    # Main Chat Window
    # -----------------------------
    window = tk.Tk()
    window.title(f"PulseChat - Logged in as [{username}]")
    window.geometry("860x620")
    window.minsize(700, 500)
    window.configure(bg="#181825")

    # State
    selected_target = [PUBLIC_TARGET]
    is_running = [True]

    # -----------------------------
    # Top Header Bar
    # -----------------------------
    header_frame = tk.Frame(window, bg="#11111b", height=50)
    header_frame.pack(fill=tk.X, side=tk.TOP)

    user_info_label = tk.Label(
        header_frame,
        text=f"👤 {username}",
        font=("Segoe UI", 12, "bold"),
        bg="#11111b",
        fg="#89b4fa"
    )
    user_info_label.pack(side=tk.LEFT, padx=16, pady=12)

    status_label = tk.Label(
        header_frame,
        text=f"● Connected to {host}:{PORT}",
        font=("Segoe UI", 9),
        bg="#11111b",
        fg="#a6e3a1"
    )
    status_label.pack(side=tk.LEFT, padx=5, pady=12)

    target_display_label = tk.Label(
        header_frame,
        text=f"Chatting with: {PUBLIC_TARGET}",
        font=("Segoe UI", 10, "bold"),
        bg="#11111b",
        fg="#f9e2af"
    )
    target_display_label.pack(side=tk.RIGHT, padx=16, pady=12)

    # -----------------------------
    # Main Content Area
    # -----------------------------
    content_frame = tk.Frame(window, bg="#181825")
    content_frame.pack(fill=tk.BOTH, expand=True, padx=14, pady=10)

    # ---- Left Panel: Chat Box ----
    chat_frame = tk.Frame(content_frame, bg="#181825")
    chat_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    chat_scrollbar = tk.Scrollbar(chat_frame)
    chat_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    chat_box = tk.Text(
        chat_frame,
        state="disabled",
        font=("Segoe UI", 10),
        bg="#1e1e2e",
        fg="#cdd6f4",
        wrap=tk.WORD,
        yscrollcommand=chat_scrollbar.set,
        relief="flat",
        padx=12,
        pady=10
    )
    chat_box.pack(fill=tk.BOTH, expand=True)
    chat_scrollbar.config(command=chat_box.yview)

    # Style tags for message highlighting
    chat_box.tag_config("system", foreground="#fab387", font=("Segoe UI", 9, "italic"))
    chat_box.tag_config("private", foreground="#cba6f7", font=("Segoe UI", 10, "bold"))
    chat_box.tag_config("public", foreground="#cdd6f4", font=("Segoe UI", 10))
    chat_box.tag_config("self", foreground="#89b4fa", font=("Segoe UI", 10, "bold"))

    # ---- Right Panel: Online Users ----
    users_panel = tk.Frame(content_frame, bg="#11111b", width=220)
    users_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=(12, 0))
    users_panel.pack_propagate(False)

    users_title = tk.Label(
        users_panel,
        text="ONLINE USERS",
        font=("Segoe UI", 10, "bold"),
        bg="#11111b",
        fg="#a6adc8"
    )
    users_title.pack(anchor="w", padx=12, pady=(12, 6))

    users_scrollbar = tk.Scrollbar(users_panel)
    users_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    users_box = tk.Listbox(
        users_panel,
        font=("Segoe UI", 10),
        bg="#181825",
        fg="#cdd6f4",
        selectbackground="#89b4fa",
        selectforeground="#11111b",
        relief="flat",
        yscrollcommand=users_scrollbar.set,
        bd=0,
        highlightthickness=0
    )
    users_box.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0, 8))
    users_scrollbar.config(command=users_box.yview)

    # Immediately add public broadcast target
    users_box.insert(tk.END, PUBLIC_TARGET)
    users_box.select_set(0)

    # Selection event for target user
    def on_select_user(event):
        selection = users_box.curselection()
        if selection:
            target = users_box.get(selection[0])
            selected_target[0] = target
            target_display_label.config(text=f"Chatting with: {target}")

    users_box.bind("<<ListboxSelect>>", on_select_user)

    # -----------------------------
    # Bottom Input Frame
    # -----------------------------
    bottom_frame = tk.Frame(window, bg="#11111b", height=65)
    bottom_frame.pack(fill=tk.X, side=tk.BOTTOM, ipady=8)

    message_entry = tk.Entry(
        bottom_frame,
        font=("Segoe UI", 11),
        bg="#313244",
        fg="#ffffff",
        insertbackground="#ffffff",
        relief="flat"
    )
    message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(14, 8), pady=10, ipady=6)
    message_entry.focus()

    def send_message():
        text = message_entry.get().strip()
        if not text:
            return

        target = selected_target[0]

        try:
            if target == PUBLIC_TARGET:
                # Normal Public Group Broadcast
                client.sendall((text + "\n").encode())
            else:
                # 1-on-1 Private Message format: PRIVATE|target|text
                full_message = f"PRIVATE|{target}|{text}\n"
                client.sendall(full_message.encode())

            message_entry.delete(0, tk.END)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to send message: {e}")

    send_btn = tk.Button(
        bottom_frame,
        text="Send",
        font=("Segoe UI", 10, "bold"),
        bg="#89b4fa",
        fg="#11111b",
        activebackground="#b4befe",
        activeforeground="#11111b",
        relief="flat",
        cursor="hand2",
        padx=18,
        command=send_message
    )
    send_btn.pack(side=tk.LEFT, padx=6, pady=10, ipady=4)

    # Clear chat log button
    def clear_chat():
        chat_box.config(state="normal")
        chat_box.delete("1.0", tk.END)
        chat_box.config(state="disabled")

    clear_btn = tk.Button(
        bottom_frame,
        text="Clear Log",
        font=("Segoe UI", 9),
        bg="#313244",
        fg="#a6adc8",
        activebackground="#45475a",
        activeforeground="#ffffff",
        relief="flat",
        cursor="hand2",
        padx=10,
        command=clear_chat
    )
    clear_btn.pack(side=tk.LEFT, padx=(4, 14), pady=10, ipady=4)

    # Press Enter to Send
    message_entry.bind("<Return>", lambda event: send_message())

    # -----------------------------
    # Message Display & Helpers
    # -----------------------------
    def display_message(message):
        chat_box.config(state="normal")

        tag = "public"
        if "[System]:" in message:
            tag = "system"
        elif "[Private" in message:
            tag = "private"

        chat_box.insert(tk.END, message + "\n", tag)
        chat_box.config(state="disabled")
        chat_box.see(tk.END)

    def update_users(users):
        users_box.delete(0, tk.END)
        # Always provide Public Broadcast at the top
        users_box.insert(tk.END, PUBLIC_TARGET)

        for u in users:
            u = u.strip()
            if u and u != username:
                users_box.insert(tk.END, u)

        # Retain currently active target if still online
        items = users_box.get(0, tk.END)
        if selected_target[0] in items:
            idx = items.index(selected_target[0])
            users_box.select_set(idx)
        else:
            selected_target[0] = PUBLIC_TARGET
            target_display_label.config(text=f"Chatting with: {PUBLIC_TARGET}")
            users_box.select_set(0)

    # -----------------------------
    # Receiver Thread (Newline-framed buffer)
    # -----------------------------
    def receive_messages():
        buffer = ""
        while is_running[0]:
            try:
                raw_data = client.recv(4096)
                if not raw_data:
                    break

                buffer += raw_data.decode("utf-8", errors="ignore")

                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    line = line.strip()
                    if not line:
                        continue

                    if line.startswith("USERS:"):
                        raw_users = line[6:].split(",")
                        window.after(0, update_users, raw_users)
                    else:
                        window.after(0, display_message, line)

            except Exception:
                break

        if is_running[0]:
            window.after(0, display_message, "[System]: Disconnected from server.")

    receiver_thread = threading.Thread(target=receive_messages, daemon=True)
    receiver_thread.start()

    # -----------------------------
    # Clean Close Handler
    # -----------------------------
    def on_closing():
        is_running[0] = False
        try:
            client.shutdown(socket.SHUT_RDWR)
        except Exception:
            pass
        try:
            client.close()
        except Exception:
            pass
        window.destroy()

    window.protocol("WM_DELETE_WINDOW", on_closing)
    window.mainloop()


if __name__ == "__main__":
    temp = tk.Tk()
    temp.withdraw()

    user = simpledialog.askstring("Username", "Enter your username:")
    temp.destroy()

    if user:
        start_chat(user.strip())