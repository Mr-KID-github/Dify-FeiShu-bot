# src/feishu_bot.py

# 导入必要的库和模块
from fastapi import APIRouter, Request, BackgroundTasks  # FastAPI相关的路由、请求和异常处理、后台任务处理
import json  # JSON处理
from src.APIs.DifyAPIs import call_dify_workflow  # 调用Dify工作流API
from src.APIs.FeiShuAPIs import FeishuAPI  # 飞书API的封装
from src.logger_setup import setup_logger  # 日志设置
from fastapi.responses import JSONResponse
import asyncio

# 初始化FeishuAPI实例
feishu_api = FeishuAPI()

# 设置日志
logger = setup_logger()

# 定义FeishuBot类，封装飞书机器人的逻辑
class FeishuBot:
    def __init__(self, name: str):
        # 初始化FeishuBot实例
        self.name = name                                        # 机器人的名称
        self.router = APIRouter()                               # 创建APIRouter实例，用于定义路由
        self.router.post("/webhook/event")(self.handle_event)   # 注册处理事件的路由

    async def handle_event(self, request: Request, background_tasks: BackgroundTasks):
        data = await request.json()
        logger.info(f"Received event: {data}")
        if 'challenge' in data:
            return {"challenge": data['challenge']}
        background_tasks.add_task(self.process_event_sync, data)
        logger.info("已经添加了一个任务到后台任务队列中，立即返回200状态码防止飞书消息重发")
        return JSONResponse(content={"status": "received"}, status_code=200)

    def process_event_sync(self, data: dict):
        # 使用 asyncio.run 执行异步方法
        asyncio.run(self.process_event(data))

    async def process_event(self, data: dict):
        logger.info(f"Processing event data: {data}")
        if "uuid" in data:
            version = "v1.0"
            event_id = data.get("uuid")
            event_type = data["event"].get("type")
        elif "schema" in data and data["schema"] == "2.0":
            version = "v2.0"
            event_id = data["header"].get("event_id")
            event_type = data["header"].get("event_type")
        else:
            logger.error("Unknown event schema")
            return
        await self.process_event_by_version(version, event_id, event_type, data)
    
    async def process_event_by_version(self, version: str, event_id: str, event_type: str, data: dict):
        handler = getattr(self, f"handle_{version.replace('.', '_')}_{event_type.replace('.', '_')}", None)
        if handler:
            await handler(event_id, data["event"])
        else:
            logger.warning(f"No handler found for event: {event_type} in version: {version}")

    # 默认处理用户和机器人的会话首次被创建事件，子类可以重写这些方法
    async def handle_v1_0_p2p_chat_create(self, event_id: str, event: dict):
        logger.info(f"Handling v1.0 p2p chat create event: {event}")
        # 默认处理逻辑

    # 默认处理消息接收事件，子类可以重写这些方法
    async def handle_v2_0_im_message_receive_v1(self, event_id: str, event: dict):
        logger.info(f"Handling v2.0 message received event: {event}")
        # 默认处理逻辑

    # 默认处理应用菜单事件，子类可以重写这些方法
    async def handle_v2_0_application_bot_menu_v6(self, event_id: str, event: dict):
        logger.info(f"Handling v2.0 application bot menu event: {event}")
        # 默认处理逻辑

    # 默认处理消息卡片操作触发事件，子类可以重写这些方法
    async def handle_v2_0_card_action_trigger(self, event_id: str, event: dict):
        logger.info(f"Handling card action trigger event: {event}")
        # 默认处理逻辑