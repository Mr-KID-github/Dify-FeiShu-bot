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
    logger.info(f"Received webhook: {data}")
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

# 处理不同版本的事件, v1.0 版本的事件处理
def handle_event_v1(event_id, event_type, data):
    logger.info(f"Received v1.0 event: {event_type}, id: {event_id}")
    if event_type == "p2p_chat_create":
        handle_p2p_chat_create_v1(data["event"])

# 处理不同版本的事件, v2.0 版本的事件处理
def handle_event_v2(event_id, event_type, data):
    logger.info(f"Received v2.0 event: {event_type}, id: {event_id}")
    if event_type == "contact.user_group.created_v3":
        handle_user_group_created_v2(data["event"])
    elif event_type == "im.message.receive_v1":
        handle_message_received_v2(data["event"])
    elif event_type == "p2p_chat_create":
        handle_p2p_chat_create_v1(data["event"])

# 处理不同版本的事件, v1.0 版本的事件处理
def handle_p2p_chat_create_v1(event):
    logger.info(f"Handling v1.0 p2p chat create event: {event}")
    initial_content = "Handling v1.0 p2p chat create event"
    chat_id = event['chat_id']
    message_response = feishu_api.send_message(chat_id, initial_content)

# 处理不同版本的事件, v2.0 版本的事件处理
def handle_user_group_created_v2(event):
    logger.info(f"Handling v2.0 user group created event: {event}")

# 处理接收到的消息
def handle_message_received_v2(event):
    logger.info(f"Handling v2.0 message received event: {event}")
    
    if (event['message']['message_type'] == "media") :
        logger.info("接收到的消息是个文件📃，调用下载文件接口")
        try:
            message_id = event['message']['message_id']
            if event['message']['message_type'] == "media":
                message_type = "file"
            else:
                message_type = "image"
            content = json.loads(event['message']['content'])  # 解析JSON字符串
            file_key = content['file_key']
            print("----------------")
            feishu_api.download_file(message_id, file_key, message_type)
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON content: {e}")
        except KeyError as e:
            logger.error(f"Error: missing key {e}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
    
    else:
        message_content = event["message"]["content"]                   # 获取消息内容
        chat_id = event["message"]["chat_id"]                           # 获取聊天 ID
        logger.info(f"Message content: {message_content}")              # 记录消息内容
        
        initial_content = "I received your message: " + message_content
        message_response = feishu_api.send_message(chat_id, initial_content, "waiting_message_card", template_variables={
            "waitText": "思考中，请稍等片刻......"
        })  # 发送消息

        message_id = message_response["data"]["message_id"]             # 获取消息 ID
        user_id = event["sender"]["sender_id"]["open_id"]               # 获取用户 ID

        response_call_dify_workflow = call_dify_workflow(               # 调用 Dify API
            query=message_content,
            user=user_id,
        )


        complete_answer_call_dify_workflow = ""  # 初始化变量
        accumulated_data = []  # 用于存储积累的数据块
        batch_size = 20  # 定义每批次的大小

        if response_call_dify_workflow.status_code == 200:              # 判断 API 调用是否成功
            for line in response_call_dify_workflow.iter_lines():       # 流式 API 返回的数据
                if line:                                                # 判断是否有数据
                    decoded_line = line.decode('utf-8')                 # 解码数据
                    if decoded_line.startswith("data:"):                # 判断是否是数据行
                        try:
                            data = json.loads(decoded_line[5:])         # 解析 JSON 数据
                            if "answer" in data:
                                complete_answer_call_dify_workflow += data["answer"]

                                accumulated_data.append(data["answer"])  # 将数据添加到累积数据列表
                                # 如果累积的数据达到批次大小，则进行一次更新
                                if len(accumulated_data) >= batch_size:
                                    feishu_api.update_message(message_id, None, "reply_message_card", template_variables={
                                        "answer": complete_answer_call_dify_workflow,
                                        "nextQ_A": "课程价格是否可以优惠？",
                                        "nextQ_B": "邹老师的联系方式是什么？",
                                        "nextQ_C": "周六的课程具体时间是什么？",
                                    })
                                    accumulated_data = []  # 清空累积数据列表
                                    logger.info(complete_answer_call_dify_workflow)
                        except json.JSONDecodeError:
                            logger.error("Failed to decode JSON line")
        else:
            logger.error(f"Error: {response_call_dify_workflow.status_code}")
            logger.error(f"Response: {response_call_dify_workflow.text}")
        # 处理剩余的累积数据
        if accumulated_data:
            feishu_api.update_message(message_id, None, "reply_message_card", template_variables={
                "answer": complete_answer_call_dify_workflow,
                "nextQ_A": "课程价格是否可以优惠？",
                "nextQ_B": "邹老师的联系方式是什么？",
                "nextQ_C": "周六的课程具体时间是什么？",
            })
            logger.info(complete_answer_call_dify_workflow)
