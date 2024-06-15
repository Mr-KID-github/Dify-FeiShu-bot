import requests
from . import APP_ID, APP_SECRET

def get_access_token():
    url = 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal'
    headers = {
        'Content-Type': 'application/json; charset=utf-8'
    }
    payload = {
        'app_id': APP_ID,
        'app_secret': APP_SECRET
    }
    response = requests.post(url, json=payload)
    response_data = response.json()
    if 'tenant_access_token' in response_data:
        return response_data['tenant_access_token']
    else:
        raise Exception('Failed to get access token:', response_data)
