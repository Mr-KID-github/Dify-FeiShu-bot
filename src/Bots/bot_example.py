# 重写Bot的消息回调方法
from src.feishu_bot import FeishuBot
from src.logger_setup import setup_logger

# 设置日志
logger = setup_logger()

# 定义ExampleBot类，继承FeishuBot
class ExampleBot(FeishuBot):
    def __init__(self, name: str):
        super().__init__(name)

    # 重写需要的事件处理方法
    async def handle_v1_0_p2p_chat_create(self, event_id: str, event: dict):
        logger.info(f"ExampleBot handling v1.0 p2p chat create event: {event}")
        # 添加你的处理逻辑

    async def handle_v2_0_im_message_receive_v1(self, event_id: str, event: dict):
        logger.info(f"ExampleBot handling v2.0 message received event: {event}")
        # 添加你的处理逻辑
