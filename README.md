# Xalert

你是一个负责刷推的AI，本体运行在一部Macmini中，任务是24小时浏览推特推荐流，当发现指定的加密alpha机会后，请你调用推送函数按指定的格式进行推送




# Xalert - 自动推特Alpha信息监控推送系统

## 项目简介

本项目是一个自动化的推特监控系统，用于24小时浏览推特推荐流，识别有价值的加密货币Alpha信息，并自动推送到Telegram群组。系统通过AI分析推文内容，筛选出具有投资价值的信息进行推送。

## 核心功能

- 🔍 自动浏览推特 ：使用浏览器自动化技术获取推特推荐流内容
- 🤖 AI智能分析 ：通过Gemini AI分析推文，识别Alpha信息
- 📱 Telegram推送 ：将有价值的信息自动推送到指定Telegram群组
- ⏰ 定时执行 ：每15分钟自动执行一次分析和推送
- 🔄 持续监控 ：24小时不间断运行

## 项目结构

```
Xalert/
├── main.py              # 主程序入口
├── browser.py            # 浏览器自动化模块
├── ai.py                 # AI分析模块
├── push.py               # Telegram推送模块
├── prompt.txt            # AI分析提示词
├── auto_run_loop.sh      # 自动运行脚本
├── 配置浏览器.sh          # 浏览器配置脚本
├── chrome_data/          # Chrome用户数据目录
├── tweets/               # 推文数据存储目录
└── README.md
```

## 环境配置

### 1. 安装依赖

```
pip install DrissionPage python-telegram-bot 
python-dotenv google-generativeai
```

### 2. 环境变量配置

在项目根目录创建 .env 文件，配置以下环境变量：

```
# Gemini AI API配置
GEMINI_API_KEY=your_gemini_api_key

# Telegram Bot配置
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHANNEL_ID=your_telegram_channel_id

# Chrome调试端口（可选）
chrome_debug_port=9777
```

### 3. 浏览器配置

首次使用需要配置浏览器并登录推特账号：

```
# 运行浏览器配置脚本
./配置浏览器.sh
```

在打开的浏览器中：

1. 访问 https://x.com/
2. 登录你的推特账号
3. 确保能正常浏览推荐流
4. 按任意键退出配置

## 使用方式

### 单次运行

```
# 执行一次完整的分析流程
python3 main.py
```

### 持续监控运行

```
# 启动自动循环脚本（每15分钟执行一次）
./auto_run_loop.sh
```

### 后台运行

```
# 使用nohup在后台运行
nohup ./auto_run_loop.sh > xalert.log 2>&1 &
```

## 运行流程

1. 浏览器启动 ： `browser.py` 启动Chrome浏览器并访问推特
2. 内容抓取 ：自动滚动推荐流，抓取推文内容并保存到 tweets/ 目录
3. AI分析 ： `ai.py` 调用Gemini AI分析推文内容，识别Alpha信息
4. 结果推送 ： `push.py` 将识别出的有价值信息推送到Telegram
5. 循环执行 ： `auto_run_loop.sh` 每15分钟重复上述流程

## 核心模块说明

### main.py - 主程序

主程序协调各个模块的工作流程：

- 调用浏览器模块获取推文
- 将推文内容传递给AI模块分析
- 处理AI返回的JSON结果
- 调用推送模块发送Alpha信息

### browser.py - 浏览器自动化

负责推特内容的自动化抓取：

- 启动Chrome浏览器并保持登录状态
- 自动滚动推荐流获取最新推文
- 解析推文结构并提取关键信息
- 将推文内容格式化为Markdown格式

### ai.py - AI分析引擎

使用Gemini AI进行智能分析：

- 读取prompt.txt中的分析提示词
- 调用Gemini API分析推文内容
- 识别具有投资价值的Alpha信息
- 返回结构化的JSON分析结果

### push.py - Telegram推送

负责将Alpha信息推送到Telegram：

- 格式化推送消息模板
- 异步发送消息到指定群组
- 处理推送失败和重试逻辑
- 支持批量推送多条Alpha信息

## AI分析规则

系统使用 `prompt.txt` 中定义的提示词进行AI分析

## 推送格式

识别到Alpha信息后，系统会以以下格式推送到Telegram：

```
🚀 Alpha信息推荐
━━━━━━━━━━━━━━━━━━━━
📊 推荐理由：[AI分析的推荐理由]

👤 发帖者：[用户全名]
🆔 用户ID：[用户ID]
⏰ 发帖时间：[距离发帖的时间]

📝 推文内容：
[原始推文内容]
```

## 自动化运行

### 定时执行脚本

`auto_run_loop.sh` 提供了完整的自动化运行方案：

- 每15分钟执行一次完整流程
- 自动切换到项目目录
- 记录执行时间和状态
- 支持长期稳定运行

### 浏览器配置脚本

`配置浏览器.sh` 用于初始化浏览器环境：

- 启动浏览器进行账号登录
- 配置用户数据持久化
- 验证推特访问权限

## 注意事项

1. 网络稳定性 ：确保网络连接稳定，推特访问正常
2. API配额 ：注意Gemini AI的API调用限制
3. 账号安全 ：使用专门的推特账号，避免影响主账号
4. 存储空间 ：定期清理 tweets/ 目录下的历史数据
5. 合规使用 ：遵守推特的使用条款和相关法律法规
6. 权限设置 ：确保脚本文件具有执行权限（chmod +x *.sh）

## 故障排除

- 浏览器启动失败 ：检查Chrome是否正确安装，端口是否被占用
- 推特登录问题 ：重新运行配置脚本，手动登录账号
- AI分析失败 ：检查API密钥是否正确，网络是否能访问Gemini服务
- 推送失败 ：验证Telegram Bot Token和频道ID是否正确
- 脚本权限问题 ：使用 chmod +x *.sh 给脚本添加执行权限

## 技术栈

- 浏览器自动化 ：DrissionPage
- AI分析 ：Google Gemini API
- 消息推送 ：python-telegram-bot
- 数据存储 ：本地文件系统
- 定时任务 ：Shell脚本
- 环境管理 ：python-dotenv
