# src/main.py
from fastapi import FastAPI
from src.feishu_bot import FeishuBot
from src.Bots.bot_dify import DifyBot
app = FastAPI()

# 创建多个飞书机器人实例并注册其路由
# example_bot = ExampleBot(name="ExampleBot")
# app.include_router(example_bot.router, prefix="/example_bot")  # 路由实际的访问路径将变成'/example_bot/webhook'

dify_bot = DifyBot(name="dify")
app.include_router(dify_bot.router, prefix="/dify") # 路由实际的访问路径将变成'/bot1/webhook'

if __name__ == "__main__":
    import uvicorn     
    uvicorn.run(app, host="0.0.0.0", port=8000)
