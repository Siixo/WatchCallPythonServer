# FCM HTTP v1 API sender

import urllib.request
import json
import os
import tempfile
import google.auth
import google.auth.transport.requests
from google.oauth2 import service_account
from config import FIREBASE_PROJECT_ID

# Scopes required for FCM API
SCOPES = ['https://www.googleapis.com/auth/cloud-platform']

def get_service_account_path():
    """Get path to service account key, either from file or environment variable."""
    # Try to read from environment variable first
    service_account_json = os.getenv('FIREBASE_SERVICE_ACCOUNT_JSON')
    if service_account_json:
        # Write to temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write(service_account_json)
            return f.name
    else:
        # Fall back to file
        return 'serviceAccountKey.json'

def send_fcm_message(token, data):
    """Send FCM message to a device token."""
    try:
        url = f"https://fcm.googleapis.com/v1/projects/{FIREBASE_PROJECT_ID}/messages:send"
        print(f"[FCM] Sending to URL: {url}")
        
        # Get access token
        access_token = get_access_token()
        print(f"[FCM] Got access token: {access_token[:20]}...")

        body = {
            "message": {
                "token": token,
                "data": data
            }
        }
        
        print(f"[FCM] Message body: {json.dumps(body)}")

        req = urllib.request.Request(
            url,
            data=json.dumps(body).encode('utf-8'),
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json; UTF-8"
            },
            method='POST'
        )

        try:
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode('utf-8'))
                print(f"[FCM] Success: {result}")
                return result
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8')
            print(f"[FCM] HTTPError {e.code}: {error_body}")
            raise Exception(f"FCM HTTP {e.code}: {error_body}")
    except Exception as e:
        print(f"[FCM] ERROR sending message: {e}")
        raise


def get_access_token():
    """Retrieve a valid access token that can be used to authorize requests.

    :return: Access token.
    """
    try:
        path = get_service_account_path()
        print(f"[FCM] Loading service account from: {path}")
        
        creds = service_account.Credentials.from_service_account_file(
            path, scopes=SCOPES)
        request = google.auth.transport.requests.Request()
        creds.refresh(request)
        
        print(f"[FCM] Got access token for project: {creds.project_id}")
        return creds.token
    except Exception as e:
        print(f"[FCM] ERROR getting access token: {e}")
        raise
