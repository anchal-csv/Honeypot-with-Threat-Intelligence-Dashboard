import json
import os
from collections import Counter

LOG_FILE = 'logs.json'

def analyze_logs():
    """Parses logs and returns aggregated threat intelligence data."""
    if not os.path.exists(LOG_FILE) or os.path.getsize(LOG_FILE) == 0:
        return {
            "total_attacks": 0,
            "top_ips": [],
            "top_usernames": [],
            "top_passwords": [],
            "top_commands": [],
            "raw_logs": []
        }

    try:
        with open(LOG_FILE, 'r') as f:
            logs = json.load(f)
    except Exception as e:
        print(f"Error reading logs: {e}")
        return None

    if not logs:
        return {
             "total_attacks": 0,
            "top_ips": [],
            "top_usernames": [],
            "top_passwords": [],
            "top_commands": [],
            "raw_logs": []
        }

    ips = []
    usernames = []
    passwords = []
    commands = []

    for entry in logs:
        ips.append(entry.get('ip'))
        usernames.append(entry.get('username'))
        passwords.append(entry.get('password'))
        cmd = entry.get('command_attempted')
        if cmd:
            commands.append(cmd)

    top_ips = Counter(ips).most_common(5)
    top_usernames = Counter(usernames).most_common(5)
    top_passwords = Counter(passwords).most_common(5)
    top_commands = Counter(commands).most_common(5)

    return {
        "total_attacks": len(logs),
        "top_ips": [{"ip": ip, "count": count} for ip, count in top_ips],
        "top_usernames": [{"username": u, "count": c} for u, c in top_usernames],
        "top_passwords": [{"password": p, "count": c} for p, c in top_passwords],
        "top_commands": [{"command": cmd, "count": c} for cmd, c in top_commands],
        "raw_logs": logs
    }

if __name__ == "__main__":
    # Test the analyzer
    data = analyze_logs()
    print(json.dumps(data, indent=2))
