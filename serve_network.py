"""
Host the Stock Analyst Intelligence Dashboard on your Local Network (LAN / Wi-Fi)
Accessible from your PC, Phone, iPad, or any device connected to the same Wi-Fi.
"""
import http.server
import socketserver
import socket
import webbrowser
import os
import sys

PORT = 8080
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def main():
    local_ip = get_ip()
    url_local = f"http://localhost:{PORT}/report.html"
    url_lan = f"http://{local_ip}:{PORT}/report.html"

    print("=" * 68)
    print(" 🚀 STOCK ANALYST INTELLIGENCE & CONSENSUS DASHBOARD SERVER")
    print("=" * 68)
    print(f" • Local PC Access:       {url_local}")
    print(f" • Phone / Network Access: {url_lan}")
    print("=" * 68)
    print(" Press Ctrl + C to stop the server.")
    print("=" * 68)

    # Optional auto-open in default browser
    try:
        webbrowser.open(url_local)
    except Exception:
        pass

    with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")

if __name__ == '__main__':
    main()
