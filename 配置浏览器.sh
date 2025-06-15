#!/bin/bash

# 获取当前脚本的目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# 跳转到脚本所在的目录
cd "$SCRIPT_DIR"

echo "已跳转到项目工作目录：$SCRIPT_DIR"

# 运行 Python 脚本
echo "正在运行 python3 ./browser.py"
python_process=$(python3 ./browser.py & echo $!)

echo "浏览器已启动。按任意键结束浏览器进程..."

# 等待用户按键
read -n 1 -s -r -p ""

# 结束 Python 进程
if ps -p $python_process > /dev/null
then
    kill $python_process
    echo "浏览器进程已结束。"
else
    echo "浏览器进程已在脚本结束前退出。"
fi

echo "脚本执行完毕。"