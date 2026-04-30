from flask import Flask, render_template, jsonify
from analyzer import analyze_logs

app = Flask(__name__)

@app.route('/')
def index():
    data = analyze_logs()
    return render_template('index.html', stats=data)

@app.route('/attackers')
def attackers():
    data = analyze_logs()
    
    # Extract unique attackers and their locations
    unique_attackers = {}
    for log in data['raw_logs']:
        ip = log.get('ip')
        if ip not in unique_attackers:
            unique_attackers[ip] = {
                'ip': ip,
                'location': log.get('location', {}),
                'attempts': 1,
                'first_seen': log.get('timestamp')
            }
        else:
            unique_attackers[ip]['attempts'] += 1
            
    return render_template('attackers.html', attackers=list(unique_attackers.values()))

@app.route('/logins')
def logins():
    data = analyze_logs()
    # Sort logs by timestamp descending
    logs = sorted(data['raw_logs'], key=lambda x: x.get('timestamp', ''), reverse=True)
    return render_template('logins.html', logs=logs)

@app.route('/api/data')
def api_data():
    """API endpoint for Chart.js"""
    return jsonify(analyze_logs())

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
