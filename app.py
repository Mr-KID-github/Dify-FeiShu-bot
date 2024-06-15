import requests
from flask import Flask, request, jsonify
# 引入DifyAPI
from src.DifyAPI import call_dify_workflow
import json
import uuid
app = Flask(__name__)

# 配置你的飞书机器人应用的 App ID 和 App Secret
APP_ID = 'cli_a6e16d43c1f0100c'
APP_SECRET = 'cA09Dt44pfUNzk6I9c3CveqDRaLvbxKA'

def convert_to_uuid(original_id):
    try:
        # Create a UUID from the original string (only works if the original string is a valid UUID format)
        new_uuid = uuid.UUID(original_id)
        return str(new_uuid)
    except ValueError:
        # If the original string is not a valid UUID format, generate a new UUID
        return str(uuid.uuid4())

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

# 发送消息（消息卡片类型）
def send_message(chat_id, content):
    access_token = get_access_token()
    url = 'https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json; charset=utf-8'
    }
    payload = {
        'receive_id': chat_id,
        'msg_type': 'interactive',
        'content': json.dumps({
            "config": {
                "wide_screen_mode": True
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "content": "I received your message: {\"text\":\"你好\"}",
                        "tag": "lark_md"
                    }
                },
                {
                    "tag": "hr"
                },
                {
                    "tag": "action",
                    "actions": [
                        {
                            "tag": "button",
                            "text": {
                                "content": "Update",
                                "tag": "plain_text"
                            },
                            "type": "default",
                            "value": {
                                "key": "update_key"
                            }
                        }
                    ]
                }
            ]
        })
    }
    response = requests.post(url, json=payload, headers=headers)
    print(f"Send Message Card response: {response.text}")
    return response.json()

# 更新消息（消息卡片类型）
def updata_message(message_id, content):
    access_token = get_access_token()
    url = f'https://open.feishu.cn/open-apis/im/v1/messages/{message_id}'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json; charset=utf-8'
    }
    payload = {
        'content': json.dumps({
            "config": {
                "wide_screen_mode": True
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "content": f"{content}",
                        "tag": "lark_md"
                    }
                },
                {
                    "tag": "hr"
                },
                {
                    "tag": "action",
                    "actions": [
                        {
                            "tag": "button",
                            "text": {
                                "content": "Update",
                                "tag": "plain_text"
                            },
                            "type": "default",
                            "value": {
                                "key": "update_key"
                            }
                        }
                    ]
                }
            ]
        })
    }
    response = requests.patch(url, json=payload, headers=headers)
    print(f"Update Message Card response: {response.text}")
    try:
        return response.json()
    except requests.exceptions.JSONDecodeError:
        print("Failed to decode JSON response")
        return response.text

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
        handle_message_received_v2(data["event"])       # 处理消息事件

def handle_p2p_chat_create_v1(event):
    print(f"Handling v1.0 p2p chat create event: {event}")
    # 添加事件处理逻辑

def handle_user_group_created_v2(event):
    print(f"Handling v2.0 user group created event: {event}")
    # 添加事件处理逻辑

def handle_message_received_v2(event):
    print(f"Handling v2.0 message received event: {event}")
    # 解析消息内容并打印
    message_content = event["message"]["content"]                   # 获取消息内容
    chat_id = event["message"]["chat_id"]                           # 获取聊天 ID
    print(f"Message content: {message_content}")
    
    # 发送初始消息卡片
    initial_content = "I received your message: " + message_content
    message_response = send_message(chat_id, initial_content)       # 发送消息
    message_id = message_response["data"]["message_id"]             # 获取消息 ID
    user_id = event["sender"]["sender_id"]["open_id"]  # 假设使用 open_id，取决于你的用户ID类型

    # 调用Dify工作流流式输出
    response_call_dify_workflow = call_dify_workflow(
        query = message_content, 
        user = user_id, 
        # conversation_id = convert_to_uuid(chat_id)      # 使用聊天 ID 作为对话 ID（需要转换为 UUID 格式）
    )

    complete_answer_call_dify_workflow = ""
    if response_call_dify_workflow.status_code == 200:
        for line in response_call_dify_workflow.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                if decoded_line.startswith("data:"):
                    try:
                        data = json.loads(decoded_line[5:])
                        if "answer" in data:
                            complete_answer_call_dify_workflow += data["answer"]
                            # 更新消息卡片
                            updata_message(message_id, complete_answer_call_dify_workflow)
                            print(data["answer"], end="", flush=True)
                    except json.JSONDecodeError:
                        print("Failed to decode JSON line")
    else:
        print(f"Error: {response_call_dify_workflow.status_code}")
        print(f"Response: {response_call_dify_workflow.text}")



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
