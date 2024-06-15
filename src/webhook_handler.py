# src/webhook_handler.py
import json
import requests
from flask import jsonify
from src.APIs.DifyAPIs import call_dify_workflow
from src.APIs.FeiShuAPIs import FeishuAPI  # 导入封装的工具类
from src.logger_setup import setup_logger   # 导入日志设置

feishu_api = FeishuAPI()  # 初始化 FeishuAPI 类
logger = setup_logger()

def handle_webhook(data):
    if data and 'challenge' in data:
        challenge = data['challenge']
        response = {
            "challenge": challenge
        }
        return jsonify(response), 200
    return jsonify({"error": "Invalid request"}), 400

def handle_event(data):
    logger.info(f"Received event: {data}")
    if not data:
        return jsonify({"error": "Invalid request"}), 400

    if data and 'challenge' in data:
        challenge = data['challenge']
        response = {
            "challenge": challenge
        }
        return jsonify(response), 200

    response = {"status": "success"}

    if "uuid" in data:
        event_id = data.get("uuid")
        event_type = data["event"].get("type")
        handle_event_v1(event_id, event_type, data)
    elif "schema" in data and data["schema"] == "2.0":
        event_id = data["header"].get("event_id")
        event_type = data["header"].get("event_type")
        handle_event_v2(event_id, event_type, data)

    return jsonify(response), 200

def handle_event_v1(event_id, event_type, data):
    logger.info(f"Received v1.0 event: {event_type}, id: {event_id}")
    if event_type == "p2p_chat_create":
        handle_p2p_chat_create_v1(data["event"])

def handle_event_v2(event_id, event_type, data):
    logger.info(f"Received v2.0 event: {event_type}, id: {event_id}")
    if event_type == "contact.user_group.created_v3":
        handle_user_group_created_v2(data["event"])
    elif event_type == "im.message.receive_v1":
        handle_message_received_v2(data["event"])
    elif event_type == "p2p_chat_create":
        handle_p2p_chat_create_v1(data["event"])

def handle_p2p_chat_create_v1(event):
    logger.info(f"Handling v1.0 p2p chat create event: {event}")
    initial_content = "Handling v1.0 p2p chat create event"
    chat_id = event['chat_id']
    message_response = feishu_api.send_message(chat_id, initial_content)

def handle_user_group_created_v2(event):
    logger.info(f"Handling v2.0 user group created event: {event}")

def handle_message_received_v2(event):
    logger.info(f"Handling v2.0 message received event: {event}")
    message_content = event["message"]["content"]
    chat_id = event["message"]["chat_id"]
    logger.info(f"Message content: {message_content}")
    
    initial_content = "I received your message: " + message_content
    message_response = feishu_api.send_message(chat_id, initial_content)
    message_id = message_response["data"]["message_id"]
    user_id = event["sender"]["sender_id"]["open_id"]

    response_call_dify_workflow = call_dify_workflow(
        query=message_content,
        user=user_id,
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
                            feishu_api.update_message(message_id, complete_answer_call_dify_workflow)
                            logger.info(data["answer"])
                    except json.JSONDecodeError:
                        logger.error("Failed to decode JSON line")
    else:
        logger.error(f"Error: {response_call_dify_workflow.status_code}")
        logger.error(f"Response: {response_call_dify_workflow.text}")
