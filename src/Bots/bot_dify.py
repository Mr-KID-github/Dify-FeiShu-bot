# 重写Bot的消息回调方法
from src.feishu_bot import FeishuBot
from src.logger_setup import setup_logger
from src.APIs.DifyAPIs import call_dify_workflow  # 调用Dify工作流API
import json  # JSON处理
from src.APIs.FeiShuAPIs import FeishuAPI  # 飞书API的封装

# 初始化FeishuAPI实例
feishu_api = FeishuAPI()

# 设置日志
logger = setup_logger()

# 定义ExampleBot类，继承FeishuBot
class DifyBot(FeishuBot):
    def __init__(self, name: str):
        super().__init__(name)

    # 重写理用户和机器人的会话首次被创建事件的方法
    async def handle_v1_0_p2p_chat_create(self, event_id: str, event: dict):
        logger.info(f"DifyBot handling v1.0 p2p chat create event: {event}")
        # 重写处理逻辑

    # 重写处理消息接受事件的方法
    async def handle_v2_0_im_message_receive_v1(self, event_id: str, event: dict):
        logger.info(f"DifyBot handling message receive event: {event}")
        # 重写处理逻辑
        try:
            message_content = event["message"]["content"]                   # 获取消息内容
            chat_id = event["message"]["chat_id"]                           # 获取聊天 ID
            logger.info(f"Message content: {message_content}")              # 记录消息内容
            
            initial_content = "I received your message: " + message_content
            
            # 发送消息等待卡片
            message_response = feishu_api.send_message(
                receive_id_type = 'chat_id',
                receive_id = chat_id,
                content = initial_content,
                card_template_name = None,
                template_variables = None,
            )  # 发送消息

            message_id = message_response["data"]["message_id"]             # 获取消息 ID
            user_id = event["sender"]["sender_id"]["open_id"]               # 获取用户 ID

            response_call_dify_workflow = call_dify_workflow(               # 调用 Dify API
                query=message_content,
                user=user_id,
            )

            # 检查返回值的类型
            logger.info(f"Response type: {type(response_call_dify_workflow)}")
            logger.info(f"Response content: {response_call_dify_workflow}")
            
            complete_answer_call_dify_workflow = ""  # 初始化变量
            accumulated_data = []  # 用于存储积累的数据块
            batch_size = 20  # 定义每批次的大小

            if response_call_dify_workflow.status_code == 200:              # 判断 API 调用是否成功
                for line in response_call_dify_workflow.iter_lines():       # 流式 API 返回的数据
                    if line:                                                # 判断是否有数据
                        decoded_line = line.decode('utf-8')                 # 解码数据
                        # print(decoded_line)
                        if decoded_line.startswith("data:"):                # 判断是否是数据行
                            try:
                                data = json.loads(decoded_line[5:])         # 解析 JSON 数据
                                if "answer" in data:
                                    complete_answer_call_dify_workflow += data["answer"]

                                    accumulated_data.append(data["answer"])  # 将数据添加到累积数据列表
                                    # 如果累积的数据达到批次大小，则进行一次更新
                                    if len(accumulated_data) >= batch_size:
                                        # print("如果累积的数据达到批次大小，则进行一次更新")
                                        feishu_api.update_message(
                                            message_id = message_id, 
                                            content = complete_answer_call_dify_workflow,
                                        )
                                        accumulated_data = []  # 清空累积数据列表
                                        logger.info(complete_answer_call_dify_workflow)
                            except json.JSONDecodeError:
                                logger.error("Failed to decode JSON line")
            else:
                logger.error(f"Error: {response_call_dify_workflow.status_code}")
                logger.error(f"Response: {response_call_dify_workflow.text}")
            # 处理剩余的累积数据
            if accumulated_data:
                # print("处理剩余的累积数据")
                feishu_api.update_message(
                    message_id = message_id, 
                    content = complete_answer_call_dify_workflow,
                )
                logger.info(complete_answer_call_dify_workflow)
        except Exception as e:
            logger.error(f"Error: missing key {e}") 

        
    # 重写处理应用菜单事件的方法
    async def handle_v2_0_application_bot_menu_v6(self, event_id: str, event: dict):
        logger.info(f"DifyBot handling application bot menu event: {event}")
        # 重写处理逻辑

    # 重写处理消息卡片操作触发事件的方法
    async def handle_v2_0_card_action_trigger(self, event_id: str, event: dict):
        logger.info(f"DifyBot handling card action trigger event: {event}")
        # 重写处理逻辑


    