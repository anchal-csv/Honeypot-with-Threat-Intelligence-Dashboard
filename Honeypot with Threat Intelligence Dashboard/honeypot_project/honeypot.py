import socket
import threading
import json
import datetime
import requests
import os

HOST = '0.0.0.0'
PORT = 2222
LOG_FILE = 'logs.json'

def get_geolocation(ip):
    """Fetches geolocation data for a given IP."""
    if ip == '127.0.0.1':
        return {"country": "Localhost", "city": "Localhost", "lat": 0, "lon": 0}
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}", timeout=3)
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'success':
                return {
                    "country": data.get("country", "Unknown"),
                    "city": data.get("city", "Unknown"),
                    "lat": data.get("lat", 0),
                    "lon": data.get("lon", 0)
                }
    except Exception as e:
        print(f"[-] Geolocation error for {ip}: {e}")
    return {"country": "Unknown", "city": "Unknown", "lat": 0, "lon": 0}

def append_to_log(log_entry):
    """Appends a log entry to the JSON log file."""
    # Ensure file exists and contains a valid array
    if not os.path.exists(LOG_FILE) or os.path.getsize(LOG_FILE) == 0:
        with open(LOG_FILE, 'w') as f:
            json.dump([], f)
    
    try:
        with open(LOG_FILE, 'r+') as f:
            data = json.load(f)
            data.append(log_entry)
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()
    except Exception as e:
        print(f"[-] Error writing to log: {e}")

def handle_client(client_socket, address):
    ip, port = address
    print(f"[!] Alert: Incoming connection from {ip}:{port}")
    
    geo_data = get_geolocation(ip)
    
    try:
        # Simulate SSH/Telnet banner
        client_socket.send(b"Ubuntu 22.04.1 LTS\n\n")
        
        # Simulate Login prompt
        client_socket.send(b"login: ")
        username = client_socket.recv(1024).decode('utf-8').strip()
        
        client_socket.send(b"Password: ")
        password = client_socket.recv(1024).decode('utf-8').strip()
        
        print(f"[*] Attempt from {ip} - User: {username}, Pass: {password}")
        
        # We deny access by default but simulate a shell for a few commands
        client_socket.send(b"\nLogin incorrect\n\n")
        
        # To gather more info, sometimes honeypots let them "in" temporarily
        # Let's pretend they got in to capture a command or two
        client_socket.send(b"Welcome to Ubuntu 22.04.1 LTS (GNU/Linux 5.15.0-53-generic x86_64)\n")
        client_socket.send(b"root@ubuntu:~# ")
        
        command = client_socket.recv(1024).decode('utf-8').strip()
        print(f"[*] Command from {ip}: {command}")
        
        # Simulate fake output
        if command:
            client_socket.send(b"bash: " + command.encode() + b": command not found\n")
            
        client_socket.close()

        # Log the attempt
        log_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "ip": ip,
            "port": port,
            "username": username,
            "password": password,
            "command_attempted": command,
            "location": geo_data
        }
        
        append_to_log(log_entry)

    except Exception as e:
        print(f"[-] Connection error with {ip}: {e}")
    finally:
        client_socket.close()

def start_honeypot():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Allow port reuse
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server.bind((HOST, PORT))
        server.listen(5)
        print(f"[*] Honeypot listening on {HOST}:{PORT}")
        
        while True:
            client_sock, addr = server.accept()
            client_handler = threading.Thread(target=handle_client, args=(client_sock, addr))
            client_handler.start()
            
    except Exception as e:
        print(f"[-] Failed to start server: {e}")
    finally:
        server.close()

if __name__ == "__main__":
    start_honeypot()
