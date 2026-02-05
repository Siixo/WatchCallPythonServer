import socket
import threading
import time
from config import SOCKET_HOST, SOCKET_PORT, PING_INTERVAL, LOGS_DIR
import os

# Variable globale pour stocker le client connecté
connected_client = None
client_lock = threading.Lock()

# Configuration des logs
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

log_file = open(f"{LOGS_DIR}/server_logs" + time.strftime("_%d_%m_%H_%M") + ".txt", "a")
log_file.write("+++++++++++++++++++++++++++++++++++++++++++++++++\n")
log_file.write(time.ctime() + "    --- Nouvelle session démarrée ---\n\n")
log_file.flush()


def log(message):
    """Write message to log file."""
    log_file.write(time.ctime() + f"  |  {message}\n")
    log_file.flush()


def handle_client(conn, addr):
    """Handle client connection (Pi)."""
    global connected_client
    
    log(f"Client connected: {addr}")
    
    with client_lock:
        connected_client = conn

    # Thread to send periodic PING
    def ping_client(c):
        try:
            while True:
                with client_lock:
                    if connected_client != c:
                        break
                try:
                    c.sendall(b'PING\n')
                except Exception as e:
                    log(f"Client déconnecté (PING failed): {addr}")   
                    break
                time.sleep(PING_INTERVAL)
        except Exception as e:
            log(f"Ping thread erreur du client {addr}: {e}")

    ping_thread = threading.Thread(target=ping_client, args=(conn,), daemon=True)
    ping_thread.start()
    
    try:
        while True:
            conn.settimeout(2)
            try:
                data = conn.recv(1024).decode().strip()
            except socket.timeout:
                continue
            
            if not data:
                break
            
            if data == "accept":
                log(f"Reçu: {data} from {addr}")
            elif data == "reject":
                log(f"Reçu: {data} from {addr}")
            elif data == "video":
                sendVideoStream(conn)
                log(f"Reçu: {data} from {addr}")
            elif data == "STOP":
                log(f"Reçu: {data} from {addr}")
                break
            else:
                conn.sendall(b"OK\n")
    
    except Exception as e:
        log(f"Erreur du client {addr}: {e}")
    finally:
        conn.close()
        with client_lock:
            connected_client = None
        log(f"Client {addr} déconnecté")


def sendVideoStream(conn):
    """Placeholder for video streaming logic."""
    return None


def start_socket_server():
    """Démarre le serveur socket pour les connexions Pi."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((SOCKET_HOST, SOCKET_PORT))
    server.listen(1)
    log(f"Serveur socket démarré sur {SOCKET_HOST}:{SOCKET_PORT}")
    
    try:
        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        server.close()
        log("Serveur socket arrêté")
