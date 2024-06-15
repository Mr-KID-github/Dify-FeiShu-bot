import requests
import json
import os
from dotenv import load_dotenv, find_dotenv

class FeishuAPI:
    def __init__(self):
        # 加载 .env 文件
        dotenv_path = find_dotenv(filename='.env', raise_error_if_not_found=True)
        load_dotenv(dotenv_path)
        
        # 从环境变量中获取 API 密钥
        self.APP_ID = os.getenv('APP_ID')
        self.APP_SECRET = os.getenv('APP_SECRET')

    def get_access_token(self):
        url = 'https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal'
        headers = {
            'Content-Type': 'application/json; charset=utf-8'
        }
        payload = {
            'app_id': self.APP_ID,
            'app_secret': self.APP_SECRET
        }
        response = requests.post(url, json=payload, headers=headers)
        response_data = response.json()
        return response_data['app_access_token']

    def send_message(self, chat_id, content):
        access_token = self.get_access_token()
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
                            "content": f"I received your message: {content}",
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

    def update_message(self, message_id, content):
        access_token = self.get_access_token()
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
