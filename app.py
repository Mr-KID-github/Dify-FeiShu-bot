from flask import Flask, request, jsonify
from src.webhook_handler import handle_webhook, handle_event
import logging
import concurrent.futures
from gevent.pywsgi import WSGIServer
import os

app = Flask(__name__)

# 创建一个线程池
executor = concurrent.futures.ThreadPoolExecutor(max_workers=10)

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    logger.info("Received webhook")
    data = request.json
    # 提交耗时任务到线程池
    executor.submit(handle_webhook, data)
    # 立即返回响应
    try:
        if data["challenge"]:
            return jsonify({"challenge": data["challenge"]}), 200
    except Exception as e:
        logger.error("Error: %s", e)
    return jsonify({"status": "received"}), 200

@app.route('/webhook/event', methods=['POST'])
def webhook_event():
    data = request.json
    # 提交耗时任务到线程池
    executor.submit(handle_event, data)
    # 立即返回响应
    print("立即返回响应")
    try:
        if data["challenge"]:
            return jsonify({"challenge": data["challenge"]}), 200
    except Exception as e:
        logger.error("Error: %s", e)
    return jsonify({"status": "received"}), 200

if __name__ == '__main__':
    logger.info("日志系统已配置，现在开始记录日志。")
    if os.getenv('FLASK_ENV') == 'development':
        app.debug = True  # 开启debug模式
    else:
        app.debug = False  # 关闭debug模式
    http_server = WSGIServer(('0.0.0.0', 5000), app)
    http_server.serve_forever()
