import os
from dotenv import load_dotenv


# 加载环境变量
load_dotenv()

# 从环境变量中获取飞书API的配置
APP_ID = os.getenv('APP_ID')
APP_SECRET = os.getenv('APP_SECRET')

# 确保环境变量已经设置
if not APP_ID or not APP_SECRET:
    raise ValueError("请确保已经设置了APP_ID和APP_SECRET环境变量")

# 导入FeiShu包中的模块
from .auth import get_access_token
from .message import send_message
from .user import get_user_info

__all__ = ['get_access_token', 'send_message']

# 初始化信息
print("FeiShu API package initialized")
