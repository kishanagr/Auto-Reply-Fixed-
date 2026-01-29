from flask import Flask, render_template, request, jsonify
from datetime import datetime
import os

app = Flask(__name__)

logs = []
is_stopped = False

@app.route('/')
def home():
    return render_template('index.html', logs=logs)

@app.route('/send', methods=['POST'])
def send():
    global is_stopped
    if is_stopped:
        return jsonify({"status": "stopped"})

    uid = request.form.get('uid')
    message = request.form.get('message')
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 🔧 TODO: Replace with actual Facebook message-sending logic
    result = f"✅ Message sent to UID {uid} at {timestamp}: {message}"
    logs.append(result)

    return jsonify({"status": "success", "log": result})

@app.route('/stop', methods=['POST'])
def stop():
    global is_stopped
    is_stopped = True
    logs.append("✋ Auto-Reply Stopped")
    return jsonify({"status": "stopped"})

@app.route('/start', methods=['POST'])
def start():
    global is_stopped
    is_stopped = False
    logs.append("▶ Auto-Reply Started")
    return jsonify({"status": "started"})

@app.route('/logs', methods=['GET'])
def get_logs():
    return jsonify({"logs": logs})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
