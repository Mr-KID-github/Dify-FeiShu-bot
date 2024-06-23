# src/main.py
from fastapi import FastAPI
from src.feishu_bot import FeishuBot

app = FastAPI()

# 创建多个飞书机器人实例并注册其路由
bot1 = FeishuBot(name="Bot1")
app.include_router(bot1.router, prefix="/bot1") # 路由实际的访问路径将变成'/bot1/webhook'

if __name__ == "__main__":
    import uvicorn      # 避免不必要的导入，提升程序的运行效率和资源管理，不过在我们这个场景下无所谓
    uvicorn.run(app, host="0.0.0.0", port=8000)
