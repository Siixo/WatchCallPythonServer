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
    url = f"https://fcm.googleapis.com/v1/projects/com.siixo.watchcallfirebase/messages:send"
    
    # Get access token
    access_token = get_access_token()

    body = {
        "message": {
            "token": token,
            "data": data
        }
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode('utf-8'),
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json; UTF-8"
        },
        method='POST'
    )

    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode('utf-8'))



def get_access_token():
    """Retrieve a valid access token that can be used to authorize requests.

    :return: Access token.
    """
    path = get_service_account_path()
    creds = service_account.Credentials.from_service_account_file(
        path, scopes=SCOPES)
    request = google.auth.transport.requests.Request()
    creds.refresh(request)
    return creds.token
