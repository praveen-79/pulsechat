import socket
import threading
from datetime import datetime

HOST = "0.0.0.0"
PORT = 5555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen()

print("=" * 55)
print(f"  PulseChat TCP Socket Server started on {HOST}:{PORT}")
print("  Waiting for client connections...")
print("=" * 55)

clients = []
usernames = []
lock = threading.Lock()


def get_timestamp():
    """Returns current time formatted as [HH:MM AM/PM]."""
    return datetime.now().strftime("[%I:%M %p]")


def send_user_list():
    """Broadcasts updated online user roster to all connected clients."""
    with lock:
        user_list = "USERS:" + ",".join(usernames) + "\n"
        for client in list(clients):
            try:
                client.sendall(user_list.encode())
            except Exception:
                pass


def broadcast_system_message(message):
    """Sends a system alert notification to all connected clients."""
    full_message = f"{get_timestamp()} [System]: {message}\n"
    print(full_message.strip())
    with lock:
        for client in list(clients):
            try:
                client.sendall(full_message.encode())
            except Exception:
                pass


def send_private_message(sender, receiver, message):
    """Routes a direct 1-on-1 private message between sender and receiver."""
    time_str = get_timestamp()
    msg_for_receiver = f"{time_str} [Private from {sender}]: {message}\n"
    msg_for_sender = f"{time_str} [Private to {receiver}]: {message}\n"

    with lock:
        # Send to receiver
        if receiver in usernames:
            idx = usernames.index(receiver)
            try:
                clients[idx].sendall(msg_for_receiver.encode())
            except Exception:
                pass

        # Send confirmation echo to sender
        if sender in usernames:
            idx = usernames.index(sender)
            try:
                clients[idx].sendall(msg_for_sender.encode())
            except Exception:
                pass


def broadcast_public_message(sender, message):
    """Broadcasts a general chat message to all connected clients."""
    full_message = f"{get_timestamp()} [Public] {sender}: {message}\n"
    print(full_message.strip())
    with lock:
        for client in list(clients):
            try:
                client.sendall(full_message.encode())
            except Exception:
                pass


def handle_client(client, address):
    """Threaded worker handling a single client connection lifecycle."""
    print(f"[+] Client connected from {address}")
    username = None
    buffer = ""

    try:
        # First received line is the username
        while "\n" not in buffer:
            chunk = client.recv(1024)
            if not chunk:
                client.close()
                return
            buffer += chunk.decode("utf-8", errors="ignore")

        username, buffer = buffer.split("\n", 1)
        username = username.strip()

        if not username:
            client.close()
            return

        with lock:
            clients.append(client)
            usernames.append(username)

        print(f"[+] '{username}' joined. Total active clients: {len(clients)}")
        broadcast_system_message(f"{username} joined the chat.")
        send_user_list()

        while True:
            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                line = line.strip()
                if not line:
                    continue

                # Check if private message format: PRIVATE|target|text
                if line.startswith("PRIVATE|"):
                    parts = line.split("|", 2)
                    if len(parts) == 3:
                        _, receiver, actual_message = parts
                        print(f"[Private] {username} -> {receiver}: {actual_message}")
                        send_private_message(username, receiver, actual_message)
                else:
                    # Public / General chat message
                    broadcast_public_message(username, line)

            raw_data = client.recv(4096)
            if not raw_data:
                break
            buffer += raw_data.decode("utf-8", errors="ignore")

    except (ConnectionResetError, ConnectionAbortedError):
        pass
    except Exception as e:
        print(f"[!] Error handling client {username or address}: {e}")
    finally:
        with lock:
            if client in clients:
                idx = clients.index(client)
                clients.remove(client)
                usernames.pop(idx)

        try:
            client.close()
        except Exception:
            pass

        if username:
            print(f"[-] '{username}' left. Total active clients: {len(clients)}")
            broadcast_system_message(f"{username} left the chat.")
            send_user_list()


def start_server():
    while True:
        try:
            client, address = server.accept()
            thread = threading.Thread(
                target=handle_client,
                args=(client, address),
                daemon=True
            )
            thread.start()
        except KeyboardInterrupt:
            print("\n[*] Server stopping...")
            break
        except Exception as e:
            print(f"[!] Server accept error: {e}")
            break

    server.close()


if __name__ == "__main__":
    start_server()