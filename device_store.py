import json
import time
from config import DEVICES_DB_PATH

# In-memory storage for devices (persists during dyno runtime on Render)
_devices_cache = None

def load_devices():
    """Load devices from JSON file or in-memory cache."""
    global _devices_cache
    
    # Return in-memory cache if it exists
    if _devices_cache is not None:
        return _devices_cache
    
    # Try to load from file
    try:
        with open(DEVICES_DB_PATH, 'r') as f:
            _devices_cache = json.load(f)
            return _devices_cache
    except (FileNotFoundError, json.JSONDecodeError):
        # Initialize empty devices dict and cache it
        _devices_cache = {"devices": []}
        return _devices_cache


def save_devices(devices):
    """Sauvegarde les appareils dans un fichier JSON et met à jour le cache."""
    global _devices_cache
    
    # Update in-memory cache
    _devices_cache = devices
    
    # Try to persist to file
    try:
        with open(DEVICES_DB_PATH, 'w') as f:
            json.dump(devices, f, indent=2)
        print(f"✓ Devices saved to {DEVICES_DB_PATH}: {len(devices.get('devices', []))} devices")
    except Exception as e:
        print(f"✗ WARNING saving to file (using in-memory cache): {e}")


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
