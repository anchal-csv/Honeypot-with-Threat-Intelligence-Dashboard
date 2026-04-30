# Honeypot-with-Threat-Intelligence-Dashboard

## Project Overview

This is a simple Python-based honeypot that captures attacker login attempts and displays the data in a web dashboard.

##  Features

* Fake login server (honeypot)
* Captures IP, username, and password
* Stores logs in JSON format
* Shows attacker data in a Flask dashboard

##  Tech Used

* Python
* Socket Programming
* Flask

##  How to Run

1. Start honeypot

```
python honeypot.py
```

2. Simulate attack

```
python attack.py
```

3. Run dashboard

```
python app.py
```

4. Open browser
   http://127.0.0.1:5000

##  Output

* Top attacker IPs
* Most used passwords

##  Note

This project is for learning purposes only.
