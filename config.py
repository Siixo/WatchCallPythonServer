# Configuration serveur
import os

# Serveur socket TCP
SOCKET_HOST = '0.0.0.0'
SOCKET_PORT = int(os.getenv('SOCKET_PORT', 8888))

# Serveur HTTP (pour l'enregistrement des tokens FCM et les alertes)
HTTP_HOST = '0.0.0.0'
HTTP_PORT = int(os.getenv('PORT', 5001))  # Render sets PORT env var

# Intervalle de ping
PING_INTERVAL = 30

# Firebase
FIREBASE_SERVICE_ACCOUNT_PATH = os.getenv('FIREBASE_SERVICE_ACCOUNT_PATH', 'serviceAccountKey.json')
FIREBASE_PROJECT_ID = os.getenv('FIREBASE_PROJECT_ID', 'watchcallfirebase')

# Stockage des appareils
DEVICES_DB_PATH = os.getenv('DEVICES_DB_PATH', 'devices.json')

# Logs
LOGS_DIR = os.getenv('LOGS_DIR', 'logs')
