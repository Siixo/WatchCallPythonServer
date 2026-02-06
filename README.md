# WatchCall Python HTTP Server

HTTP server for Render cloud deployment. Handles FCM token registration and alert delivery to Android phones.

## Features

- POST `/api/register_fcm_token` - Register Android phone FCM token
- POST `/api/alert` - Send alert to registered phones
- Firebase Cloud Messaging integration
- In-memory device storage (persists during deployment)

## Environment Variables

- `FIREBASE_SERVICE_ACCOUNT_JSON` - Firebase service account credentials (required)
- `FIREBASE_PROJECT_ID` - Firebase project ID (default: `watchcallfirebase`)
- `PORT` - HTTP server port (default: `5001`, Render sets this automatically)

## Deployment

Deployed on Render.com at: https://watchcallpythonserver.onrender.com

## Running Locally

```bash
python main.py
```
