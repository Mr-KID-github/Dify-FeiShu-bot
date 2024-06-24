# Dify-FeiShu-bot

Dify-FeiShu-bot是一个使用python Flask框架编写的后端，可以非常方便的支持利用Dify接入飞书搭建飞书机器人，并且充分利用飞书消息卡片，可以搭建出漂亮的UI界面

![墨趣书法Agent展示效果图](./static/images/墨趣书法Agent展示效果图.png)

# 项目特点：
1. 非常方便创建bot；
2. 非常方便创建消息卡片；

# 安装运行
1. 克隆项目
    ```bash
    git clone https://github.com/Mr-KID-github/Dify-FeiShu-bot.git
    ```

2. 修改项目环境配置
    将.env.example改为.env，并修改里面的环境变量，配置你自己的Dify密钥和飞书机器人相关配置

3. 创建虚拟环境
    ```bash
    conda create --name DifyOnFeishu python=3.12
    ```

4. 激活虚拟环境
    ```bash
    conda activate DifyOnFeishu
    ```

5. 安装依赖
    ```bash
    pip install -r requirements.txt
    ```

6. 运行 FastAPI 服务器：
    - 使用 uvicorn 运行你的应用：

        ```bash
        uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
        ```

        或者你可以直接使用：
        ```bash
        ./start.sh
        ```
    - 这会启动一个本地服务器，你可以在浏览器中访问 http://127.0.0.1:8000/docs#/ 查看接口文档。

7. 如果是在本地调试的话，你可以使用 ngrok 暴露本地服务器：（可选，并且需要注意的是⚠️每次ngrok生成的URL都会变动，所以也需要同步更新飞书机器人的事件回调配置）
    - 为了让飞书可以访问你的本地服务器，需要使用 ngrok 暴露本地服务器到公网。
    - 下载并安装 ngrok，然后运行以下命令：

        ```bash
        ngrok http 8000
        ```
    这会生成一个公网 URL，例如 https://abc123.ngrok.io，将这个 URL 配置为飞书机器人的 webhook URL。

8. 配置飞书机器人的事件回调：
    
    登录飞书开发者后台，找到你的机器人应用，进入配置页面。在 【事件与回调】的webhook 配置中，将上一步得到的 ngrok 公网 URL 配置进去，你的 webhook 路由已经配置为 /`your_bot_name`/webhook/event，因此飞书的 webhook URL 应该是：例如 
    ```bash
    https://abc123.ngrok.io/your_bot_name/webhook/event
    ```

    如果是在远程服务器（例如阿里云、腾讯云、火山引擎等有公网IP地址，更建议此方案），可以使用域名，也可以使用IP加端口的方式配置飞书的 webhook URL 应该是：例如 
    ```bash
    http://your_ip:your_port/your_bot_name/webhook/event

    或者

    https://your_ip:your_port/your_bot_name/webhook/event
    ```

如果飞书机器人的事件回调配置通过✅，那就恭喜你🎉你，基本配置已经完成了。

# 项目的基础配置和使用
## 配置.env
首先你可以参考`.env.example`里面的配置在项目根目录新建一个`.env`文件。关于里面的配置详解，请查阅：[关于env环境配置](./docs/关于env环境配置.md)







# 其他
在运行应用之前，可以在终端中使用export命令设置环境变量，例如

```shell 
export APP_ENV=development
```
这个是以开发环境运行应用的意思。详情🔎请见：[关于start.sh脚本启动应用](./docs/关于start.sh脚本启动应用.md)