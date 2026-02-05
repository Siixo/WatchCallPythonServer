import urllib.request
import json
from socket_handler import connected_client, client_lock
from socket_handler import log

def send_alert_http(pi_id, message, alert_type):
    url = "http://localhost:5001/api/alert"

    data = {
        "pi_id": pi_id,
        "message": message,
        "alert_type": alert_type
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode('utf-8'),
        headers={
            "Content-Type": "application/json; UTF-8"},
        method='POST'
    )

    try:
        with urllib.request.urlopen(req) as response:
            resp_data = json.loads(response.read().decode('utf-8'))
            print(f'Alerte envoyée avec succès: {resp_data}')
    except Exception as e:
        print(f'Error sending alert: {e}')  
    
def listen_for_user_input():
    """Unified input listener for both socket (1) and HTTP/FCM (2) alerts."""
    while True:
        try:
            user_input = input("\nPress '1' for socket alarm, '2' for FCM alert: ").strip()
            
            if user_input == '1':
                # Send socket alarm
                with client_lock:
                    if connected_client:
                        try:
                            connected_client.sendall(b'ALARM\n')
                            log("Alarme envoyée au client via socket")
                            print("Socket alarm sent!")
                        except Exception as e:
                            log(f"Erreur lors de l'envoi de l'alarme au client: {e}")
                            print(f"Error sending socket alarm: {e}")
                    else:
                        log("Aucun client connecté pour envoyer l'alarme")
                        print("No client connected for socket alarm")
            
            elif user_input == '2':
                # Send FCM alert
                pi_id = input("Enter pi_id: ").strip()
                message = input("Enter message: ").strip() or "Motion detected"
                alert_type = input("Enter alert_type: ").strip() or "motion"
                send_alert_http(pi_id, message, alert_type)
                
        except EOFError:
            print("User input ended")
            break
        except Exception as e:
            print(f"Input error: {e}")