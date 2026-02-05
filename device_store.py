import json
import time
from config import DEVICES_DB_PATH

def load_devices():
    """Load devices from JSON file."""
    try:
        with open(DEVICES_DB_PATH, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"devices": []}


def save_devices(devices):
    """Sauvegarde les appareils dans un fichier JSON."""
    try:
        with open(DEVICES_DB_PATH, 'w') as f:
            json.dump(devices, f, indent=2)
        print(f"✓ Devices saved to {DEVICES_DB_PATH}: {len(devices.get('devices', []))} devices")
    except Exception as e:
        print(f"✗ ERROR saving devices: {e}")


def register_device(fcm_token, pi_id):
    """Enregistre un appareil avec son token FCM et l'ID du Pi."""
    devices = load_devices()
    
    # Vérifie si le token existe déjà
    for device in devices["devices"]:
        if device["fcm_token"] == fcm_token:
            device["pi_id"] = pi_id
            save_devices(devices)
            return device
    
    # Ajoute un nouvel appareil
    device = {
        "fcm_token": fcm_token,
        "pi_id": pi_id,
        "registered_at": str(time.time())
    }
    devices["devices"].append(device)
    save_devices(devices)
    return device


def get_devices_for_pi(pi_id):
    """Récupère tous les tokens FCM pour un ID de Pi spécifique."""
    devices = load_devices()
    return [d["fcm_token"] for d in devices["devices"] if d["pi_id"] == pi_id]


def remove_device(fcm_token):
    """Supprime un appareil du stockage."""
    devices = load_devices()
    devices["devices"] = [d for d in devices["devices"] if d["fcm_token"] != fcm_token]
    save_devices(devices)
