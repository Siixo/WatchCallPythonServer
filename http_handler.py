# HTTP Handler for FCM token registration and alerts
# To be implemented

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from device_store import register_device, get_devices_for_pi, remove_device
from fcm_sender import send_fcm_message, get_access_token
from config import HTTP_HOST, HTTP_PORT

class HTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            if self.path == '/api/register_fcm_token':
                content_length = int(self.headers.get('Content-Length', 0))

                body = self.rfile.read(content_length)

                data = json.loads(body.decode('utf-8'))
                fcm_token = data.get('fcm_token')
                pi_id = data.get('pi_id')

                if not fcm_token or not pi_id:
                    self.send_response(400)
                    self.end_headers()
                    self.wfile.write(b'Missing fcm_token or pi_id')
                    print("Error: Missing fcm_token or pi_id")
                    return
                
                register_device(fcm_token, pi_id)
                print(f"Device registered: token={fcm_token[:20]}..., pi_id={pi_id}")

                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {'status': 'Appareil enregistré avec succès'}
                self.wfile.write(json.dumps(response).encode('utf-8'))
            
            elif self.path == '/api/alert':
                content_length = int(self.headers.get('Content-Length', 0))

                body = self.rfile.read(content_length)

                data = json.loads(body.decode('utf-8'))
                pi_id = data.get('pi_id')

                if not pi_id:
                    self.send_response(400)
                    self.end_headers()
                    self.wfile.write(b'Missing pi_id')
                    print("Error: Missing pi_id")
                    return
                
                tokens = get_devices_for_pi(pi_id)
                print(f"Found {len(tokens)} tokens for pi_id={pi_id}")

                for token in tokens:
                    data_payload = {'alert': 'ALARM'}
                    try:
                        response = send_fcm_message(token, data_payload)
                        print(f'Notification envoyée au token {token[:20]}...: {response}')
                    except Exception as e:
                        print(f'Erreur lors de l\'envoi de la notification au token {token[:20]}...: {e}')

                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {'status': 'Alertes envoyées avec succès', 'tokens_count': len(tokens)}
                self.wfile.write(json.dumps(response).encode('utf-8'))
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b'La route n\'existe pas')
        except Exception as e:
            print(f"ERROR in do_POST: {e}")
            self.send_response(500)
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))


def start_http_server():
    """Démarrage du serveur HTTP."""
    server = HTTPServer((HTTP_HOST, HTTP_PORT), HTTPRequestHandler)
    print(f"Démarrage du serveur HTTP sur {HTTP_HOST}:{HTTP_PORT}")
    server.serve_forever()





