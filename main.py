#!/usr/bin/env python3
"""
WatchCall HTTP Server - Render Deployment
Handles:
- FCM token registration from Android phones
- Alert delivery to phones via FCM
"""

from http_handler import start_http_server


def main():
    """Start HTTP server (for Render cloud deployment)"""
    print("=" * 60)
    print("WatchCall - HTTP Server (Render)")
    print("=" * 60)
    start_http_server()


if __name__ == "__main__":
    main()
