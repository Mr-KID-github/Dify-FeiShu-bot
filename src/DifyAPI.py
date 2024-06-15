import requests
from dotenv import load_dotenv, find_dotenv
import os
import json

# 加载 .env 文件
dotenv_path = find_dotenv(filename='.env', raise_error_if_not_found=True)
load_dotenv(dotenv_path)

# 从环境变量中获取 API 密钥
API_KEY = os.getenv('DIFY_API_KEY')

def call_dify_workflow(query, user, conversation_id="", response_mode="streaming", files=[]):
    url = 'https://api.hackathon.difyai.com/v1/chat-messages'
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }
    payload = {
        "inputs": {
            'teching_points': '荣和教学点'
        },
        "query": query,
        "response_mode": response_mode,
        "conversation_id": conversation_id,
        "user": user,
        "files": files
    }
    response = requests.post(url, json=payload, headers=headers, stream=True)
    
    return response

def process_streaming_response(response):
    complete_answer = ""
    if response.status_code == 200:
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                if decoded_line.startswith("data:"):
                    try:
                        data = json.loads(decoded_line[5:])
                        if "answer" in data:
                            complete_answer += data["answer"]
                            print(data["answer"], end="", flush=True)
                    except json.JSONDecodeError:
                        print("Failed to decode JSON line")
    else:
        print(f"Error: {response.status_code}")
        print(f"Response: {response.text}")
        
    return complete_answer

# 示例调用
if __name__ == "__main__":
    query = "What are the specs of the iPhone 13 Pro Max?"
    user = "abc-123"
    files = [
        # {
        #     "type": "image",
        #     "transfer_method": "remote_url",
        #     "url": "https://cloud.dify.ai/logo/logo-site.png"
        # }
    ]
    
    response = call_dify_workflow(query, user, files=files)
    complete_answer = process_streaming_response(response)
    print("\nComplete Answer:", complete_answer)
