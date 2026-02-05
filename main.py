import threading
from socket_handler import start_socket_server
from http_handler import start_http_server
from tests.console_tester import send_alert_http, listen_for_user_input

def main():
    """Démarrage des serveurs socket et HTTP."""
    
    # Start socket server for Pi connections (daemon thread)
    socket_thread = threading.Thread(target=start_socket_server, daemon=True)
    socket_thread.start()
    
    # Start HTTP server for FCM token registration and alerts (daemon thread)
    http_thread = threading.Thread(target=start_http_server, daemon=True)
    http_thread.start()
    
    # Run user input listener on main thread (blocks here)
    #listen_for_user_input()


if __name__ == "__main__":
    main()
