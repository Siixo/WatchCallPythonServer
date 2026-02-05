# Server_tcp.py depracated code, gardé pour référence uniquement
""" import socket
import threading
import time
import firebase_admin
from firebase_admin import credentials

HOST = '0.0.0.0'
PORT = 8888

cred = credentials.Certificate("path/to/serviceAccountKey.json")
firebase_admin.initialize_app(cred)

# Intervalle d'envoi du PING (en secondes)
PING_INTERVAL = 30

# Global variable to store the connected client
connected_client = None
client_lock = threading.Lock()

# Logs writing
file = open("logs/server_logs" + time.strftime("_%d_%m_%H_%M") + ".txt", "a")
file.write("+++++++++++++++++++++++++++++++++++++++++++++++++\n")
file.write(time.ctime() + "    --- Nouvelle session démarrée ---\n\n")
file.flush()

def listen_for_user_input():
    #Listen for user input in a separate thread to send alarms
    global connected_client
    
    while True:
        try:
            user_input = input("Press 1 to send an alarm: ")
            if user_input.strip() == '1':
                with client_lock:
                    if connected_client:
                        try:
                            connected_client.sendall(b'ALARM\n')
                            #print("Alarm sent to client")
                        except Exception as e:
                            #print(f"Error sending alarm: {e}")
                            file.write(time.ctime() + "  |  Erreur lors de l'envoi de l'alarme au client \n")
                            file.flush()
                    else:
                        #print("No client connected to send alarm")
                        file.write(time.ctime() + "  |  Aucun client connecté pour envoyer l'alarme \n")
                        file.flush()
                    
        except EOFError:
            file.write(time.ctime() + "  |  Fin de l'entrée utilisateur détectée \n")
            file.flush()
            break
        except Exception as e:
            #print(f"Error: {e}")
            file.write(time.ctime() + f"  |  Erreur d'entrée utilisateur: {e} \n")
            file.flush()

def handle_client(conn, addr):
    global connected_client
    
    #print(f"\nClient connected: {addr} à " + time.ctime())
    file.write(time.ctime() + f"  |  Client connected: {addr} à " + time.ctime() + " \n")
    file.flush()
    
    with client_lock:
        connected_client = conn

    # Thread qui envoie périodiquement des PING au client connecté
    def ping_client(c):
        try:
            while True:
                with client_lock:
                    if connected_client != c:
                        break
                try:
                    #print("PING envoyé à " + str(addr) + " à " + time.ctime())
                    c.sendall(b'PING\n')
                except Exception as e:
                    #print(f"Error sending PING: {e}")
                    file.write(time.ctime() + f"  |  Client deconnecté (PING failed): {addr} \n")
                    file.flush()   
                    break
                time.sleep(PING_INTERVAL)
        except Exception as e:
            #print(f"Ping thread error: {e}")
            file.write(time.ctime() + f"  |  Ping thread erreur du client {addr}: \n")
            file.flush()

    ping_thread = threading.Thread(target=ping_client, args=(conn,), daemon=True)
    ping_thread.start()
    
    try:
        while True:
            conn.settimeout(2)
            try:
                data = conn.recv(1024).decode().strip()
            except socket.timeout:
                break  # Timeout reached, go back to the beginning of the loop to check for PING sending
                file.write(time.ctime() + f"  |  Timeout d'attente des données du client {addr} \n")
                file.flush()
            
            if not data:
                break
            
            #print(f"Received: {data}", " à: " + time.ctime())
            
            
            if data == "accept":
                #print("Le message d'acceptation a été reçu")
                file.write(time.ctime() + f"  |  Reçu: {data} from {addr} \n")
                file.flush()
            if data == "reject":
                #print("Le message de rejet a été reçu")
                file.write(time.ctime() + f"  |  Reçu: {data} from {addr} \n")
                file.flush()
            if data == "video":
                #print("Demande de flux vidéo reçue")
                sendVideoStream(conn)
                file.write(time.ctime() + f"  |  Reçu: {data} from {addr} \n")
                file.flush()
            elif data == "STOP":
                #print("STOP received - closing connection")
                file.write(time.ctime() + f"  |  Reçu: {data} from {addr} \n")
                file.flush()
                break
            else:
                conn.sendall(b"OK\n")
    
    except Exception as e:
        #print(f"Error: {e}")
        file.write(time.ctime() + f"  |  Erreur du client {addr}: {e} \n")
        file.flush()
    finally:
        conn.close()
        with client_lock:
            connected_client = None
        #print(f"Client {addr} disconnected")
        file.write(time.ctime() + f"  |  Client {addr} déconnecté \n")
        file.flush()


def sendVideoStream(conn):
    return None  # Placeholder for video streaming logic






def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(1)
    #print(f"Server started on {HOST}:{PORT}")
    file.write(time.ctime() + f"  |  Serveur démarré sur {HOST}:{PORT} \n")
    
    # Start input listener thread
    input_thread = threading.Thread(target=listen_for_user_input, daemon=True)
    input_thread.start()
    
    try:
        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        server.close()

if __name__ == "__main__":
    start_server()

 """