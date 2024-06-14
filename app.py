import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# 配置你的飞书机器人应用的 App ID 和 App Secret
APP_ID = 'cli_a6e16d43c1f0100c'
APP_SECRET = 'cA09Dt44pfUNzk6I9c3CveqDRaLvbxKA'

# 获取飞书 API 的访问令牌
def get_access_token():
    url = 'https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal'
    headers = {
        'Content-Type': 'application/json; charset=utf-8'
    }
    payload = {
        'app_id': APP_ID,
        'app_secret': APP_SECRET
    }
    response = requests.post(url, json=payload, headers=headers)
    response_data = response.json()
    return response_data['app_access_token']

# 发送消息
def send_message(chat_id, content):
    access_token = get_access_token()
    url = 'https://open.feishu.cn/open-apis/message/v4/send/'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json; charset=utf-8'
    }
    payload = {
        'chat_id': chat_id,
        'msg_type': 'text',
        'content': {
            'text': content
        }
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

# 处理飞书的 URL 验证请求
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if data and 'challenge' in data:
        challenge = data['challenge']
        response = {
            "challenge": challenge
        }
        return jsonify(response), 200
    return jsonify({"error": "Invalid request"}), 400

# 处理飞书的事件推送请求
@app.route('/webhook/event', methods=['POST'])
def webhook_event():
    data = request.json
    print(f"Received event: {data}")
    if data and 'challenge' in data:
        challenge = data['challenge']
        response = {
            "challenge": challenge
        }
        return jsonify(response), 200

    if not data:
        return jsonify({"error": "Invalid request"}), 400

    # 初始化一个默认的 response
    response = {"status": "success"}

    # 处理 v1.0 版本的事件
    if "uuid" in data:
        event_id = data.get("uuid")
        event_type = data["event"].get("type")
        handle_event_v1(event_id, event_type, data)
    # 处理 v2.0 版本的事件
    elif "schema" in data and data["schema"] == "2.0":
        event_id = data["header"].get("event_id")
        event_type = data["header"].get("event_type")
        handle_event_v2(event_id, event_type, data)

    return jsonify(response), 200

def handle_event_v1(event_id, event_type, data):
    print(f"Received v1.0 event: {event_type}, id: {event_id}")
    # 根据 event_type 处理不同的事件
    if event_type == "p2p_chat_create":
        handle_p2p_chat_create_v1(data["event"])

def handle_event_v2(event_id, event_type, data):
    print(f"Received v2.0 event: {event_type}, id: {event_id}")
    # 根据 event_type 处理不同的事件
    if event_type == "contact.user_group.created_v3":
        handle_user_group_created_v2(data["event"])
    elif event_type == "im.message.receive_v1":
        handle_message_received_v2(data["event"])

def handle_p2p_chat_create_v1(event):
    print(f"Handling v1.0 p2p chat create event: {event}")
    # 添加事件处理逻辑

def handle_user_group_created_v2(event):
    print(f"Handling v2.0 user group created event: {event}")
    # 添加事件处理逻辑

def handle_message_received_v2(event):
    print(f"Handling v2.0 message received event: {event}")
    # 解析消息内容并打印
    message_content = event["message"]["content"]
    chat_id = event["message"]["chat_id"]
    print(f"Message content: {message_content}")
    
    # 发送回复消息
    reply_content = "I received your message: " + message_content
    send_message(chat_id, reply_content)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
