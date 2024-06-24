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