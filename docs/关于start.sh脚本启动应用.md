# 关于start.sh脚本启动应用

你可以通过在 start.sh 脚本中使用条件语句来根据环境变量动态调整 uvicorn 命令的参数。下面是一个示例  `start.sh` 脚本，展示了如何根据环境变量配置动态刷新：

### 示例 `start.sh`
```bash
#!/bin/bash

# 检查环境变量是否设置
if [ -z "$APP_ENV" ]; then
  echo "APP_ENV 环境变量未设置，使用默认模式 'development'."
  APP_ENV="development"
fi

# 根据环境变量设置不同的启动命令
if [ "$APP_ENV" == "development" ]; then
  echo "启动开发模式..."
  uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
elif [ "$APP_ENV" == "production" ]; then
  echo "启动生产模式..."
  uvicorn src.main:app --host 0.0.0.0 --port 8000
else
  echo "未知的 APP_ENV 值: $APP_ENV. 使用默认开发模式."
  uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
fi
```
### 使用方法
1. 设置环境变量：
    
    在启动 start.sh 之前，通过以下命令设置环境变量 APP_ENV：

    ```bash
    export APP_ENV=development  # 或者 production
    ```
2. 运行脚本：

    通过以下命令运行脚本：

    ```bash
    ./start.sh
    ```
### 解释
- 检查环境变量：脚本首先检查 `APP_ENV` 环境变量是否设置。如果未设置，则默认为 `development`。

- 根据环境变量设置启动命令：脚本根据 `APP_ENV` 的值选择不同的 `uvicorn` 启动命令。如果 `APP_ENV` 为 `development`，则使用 `--reload` 选项启用自动重载。如果 `APP_ENV` 为 `production`，则不使用 `--reload` 选项。

- 运行 `uvicorn` 命令：根据选择的模式运行相应的 `uvicorn` 命令。

这样，你就可以通过设置环境变量来动态调整 `uvicorn` 的执行命令，适应不同的开发和生产环境。如果需要更多的环境变量或配置选项，可以在脚本中添加更多的条件语句和选项。