from flask import Flask, request
from src.webhook_handler import handle_webhook, handle_event
from src.logger_setup import setup_logger   # 导入日志设置

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    return handle_webhook(data)

@app.route('/webhook/event', methods=['POST'])
def webhook_event():
    data = request.json
    return handle_event(data)

if __name__ == '__main__':
    logger = setup_logger()
    logger.info("日志系统已配置，现在开始记录日志。")
    app.run(host='0.0.0.0', port=5000, debug=True)
