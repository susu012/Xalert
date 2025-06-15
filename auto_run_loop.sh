#!/bin/bash

# 动态获取脚本所在的目录（即项目根目录）
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROGRAM_DIR="$SCRIPT_DIR"

# 定义要执行的命令
COMMAND="python3 main.py"

# 定义执行间隔（15分钟 = 900秒）
INTERVAL=900

echo "=== Xalert 定时执行脚本启动中 ==="
echo "脚本位置: $SCRIPT_DIR"
echo "程序目录: $PROGRAM_DIR"
echo "执行命令: $COMMAND"
echo "执行间隔: ${INTERVAL}秒 (15分钟)"
echo "-----------------------------------"

while true; do
  TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
  echo "$TIMESTAMP: 正在执行程序..."
  
  # 切换到程序目录并执行命令
  cd "$PROGRAM_DIR" && $COMMAND
  
  # 程序执行完成后的提示
  TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
  echo "$TIMESTAMP: 程序执行完成。将在 ${INTERVAL} 秒后再次执行..."
  
  # 等待15分钟
  sleep $INTERVAL
done