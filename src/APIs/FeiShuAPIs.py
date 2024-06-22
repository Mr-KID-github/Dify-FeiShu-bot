import requests
import json
import os
from dotenv import load_dotenv, find_dotenv
from src.APIs.OSSAPIs import OSSManager

class FeishuAPI:
    def __init__(self):
        # 加载 .env 文件
        dotenv_path = find_dotenv(filename='.env', raise_error_if_not_found=True)
        load_dotenv(dotenv_path)
        
        # 从环境变量中获取 API 密钥
        self.APP_ID = os.getenv('APP_ID')
        self.APP_SECRET = os.getenv('APP_SECRET')

        # 从环境变量中获取卡片模板
        feishu_card_templates_str = os.getenv('FEISHU_CARD_TEMPLATES')
        self.FEISHU_CARD_TEMPLATES = json.loads(feishu_card_templates_str)
    
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

    def send_message(self, receive_id_type, receive_id, content=None, card_template_name=None, template_variables=None):
        access_token = self.get_access_token()

        # Check if a card template is available for the message
        if card_template_name:
            card_template = self.FEISHU_CARD_TEMPLATES.get(card_template_name)
            if not card_template:
                logger.warning(f"No card template found for name: {card_template_name}, using default message.")
                card_template_name = None  # Reset to use default message
            else:
                # Set template variables if provided
                if template_variables:
                    for key, value in template_variables.items():
                        card_template['template_variable'][key] = value
                
                # Construct the template content
                card_content = {
                    "type": "template",
                    "data": {
                        "template_id": card_template["template_id"],
                        "template_variable": card_template["template_variable"]
                    }
                }
                payload_content = json.dumps(card_content)

        if not card_template_name:
            # Default content if no template is used
            payload_content = json.dumps({
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

        url = f'https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type={receive_id_type}'
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json; charset=utf-8'
        }
        payload = {
            'receive_id': receive_id,
            'msg_type': 'interactive',
            'content': payload_content
        }

        response = requests.post(url, json=payload, headers=headers)
        print(f"Send Message Card response: {response.text}")
        return response.json()

    # Update a message card with new content
    def update_message(self, message_id, content=None, card_template_name=None, template_variables=None):
        access_token = self.get_access_token()
        try:
            # Check if a card template is available for the message
            if card_template_name:
                card_template = self.FEISHU_CARD_TEMPLATES.get(card_template_name)
                if not card_template:
                    logger.warning(f"No card template found for name: {card_template_name}, using default message.")
                    card_template_name = None  # Reset to use default message
                else:
                    # Set template variables if provided
                    if template_variables:
                        for key, value in template_variables.items():
                            card_template['template_variable'][key] = value
                    
                    # Construct the template content
                    card_content = {
                        "type": "template",
                        "data": {
                            "template_id": card_template["template_id"],
                            "template_variable": card_template["template_variable"]
                        }
                    }
                    payload_content = json.dumps(card_content)
        except Exception as e:
            logger.error(f"Error: missing key {e}") 

        # if not card_template_name:
        #     # Default content if no template is used
        #     payload_content = json.dumps({
        #         "config": {
        #             "wide_screen_mode": True
        #         },
        #         "elements": [
        #             {
        #                 "tag": "div",
        #                 "text": {
        #                     "content": f"I received your message: {content}",
        #                     "tag": "lark_md"
        #                 }
        #             },
        #             {
        #                 "tag": "hr"
        #             },
        #             {
        #                 "tag": "action",
        #                 "actions": [
        #                     {
        #                         "tag": "button",
        #                         "text": {
        #                             "content": "Update",
        #                             "tag": "plain_text"
        #                         },
        #                         "type": "default",
        #                         "value": {
        #                             "key": "update_key"
        #                         }
        #                     }
        #                 ]
        #             }
        #         ]
        #     })

        url = f'https://open.feishu.cn/open-apis/im/v1/messages/{message_id}'
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json; charset=utf-8'
        }
        payload = {
            'content': payload_content
        }
        response = requests.patch(url, json=payload, headers=headers)
        print(f"Update Message Card response: {response.text}")
        try:
            return response.json()
        except requests.exceptions.JSONDecodeError:
            print("Failed to decode JSON response")
            return response.text
    
    def download_file(self, message_id, file_key, type):
        print("开始下载文件")
        access_token = self.get_access_token()
        url = f'https://open.feishu.cn/open-apis/im/v1/messages/{message_id}/resources/{file_key}?type={type}'
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        response = requests.get(url, headers=headers)
        print("response是这个：", response)
        if response.status_code == 200:
            # 假设下载的是视频文件，根据实际情况调整文件扩展名
            # 假设下载的是视频文件，根据实际情况调整文件扩展名
            download_dir = os.path.abspath(os.path.join(os.getcwd(), '..', 'Downloads'))
            os.makedirs(download_dir, exist_ok=True)
            file_name = f"{file_key}.mp4"
            file_path = os.path.join(download_dir, file_name)
            
            with open(file_path, 'wb') as f:
                f.write(response.content)
                print(file_path)
                # 调用oss上传服务器
                # 创建OSSManager实例
                access_key_id = 'LTAI5tS5YkBn4yHHFkYNydea'
                access_key_secret = '6U1eJsGb0ivlSfA6CJbQuVLHLcAIhJ'
                endpoint = 'https://oss-cn-shenzhen.aliyuncs.com'  # 深圳节点的Endpoint
                bucket_name = 'bucket-feishu'
                oss_manager = OSSManager(access_key_id, access_key_secret, endpoint, bucket_name)

                # OSS上的目录前缀
                oss_key_prefix = 'video/' + file_name

                # 上传文件
                upload_status = oss_manager.upload_file(file_path, oss_key_prefix)
                if upload_status == 200:
                    print(f"File uploaded successfully to OSS as {oss_key_prefix}")
                else:
                    print(f"Failed to upload file to OSS. Status code: {upload_status}")

            print(f"File downloaded successfully as {file_name}")
            return file_name
        else:
            print(f"Failed to download file. Status code: {response.status_code}, Response: {response.text}")
            return None
