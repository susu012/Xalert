import os
import telegram
import asyncio
from dotenv import load_dotenv

def push_alpha_to_telegram(tweet_data, message_index=None, total_count=None):
    """
    将Alpha信息推送到Telegram群组
    
    参数:
        tweet_data: 包含推荐推文信息的字典，包含以下字段：
                   - recommendation_reason: 推荐理由
                   - username: 发帖者全名
                   - author_id: @开头的用户ID
                   - time_since_published: 距离发帖的时间
                   - tweet_text: 推文内容
        message_index: 当前消息序号（可选）
        total_count: 总消息数量（可选）
    """
    # 加载环境变量
    load_dotenv()
    
    # 从环境变量获取Telegram配置
    telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    telegram_channel_id = os.getenv("TELEGRAM_CHANNEL_ID")
    
    if not telegram_bot_token or not telegram_channel_id:
        raise ValueError("环境变量中缺少TELEGRAM_BOT_TOKEN或TELEGRAM_CHANNEL_ID")
    
    # 转换channel_id为整数（如果是负数需要保持负号）
    try:
        channel_id = int(telegram_channel_id)
    except ValueError:
        raise ValueError("TELEGRAM_CHANNEL_ID必须是有效的整数")
    
    # 构建消息头部（包含序号）
    header = ""
    if message_index is not None:
        if total_count is not None:
            header = f"第 {message_index} 条 (共 {total_count} 条)\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        else:
            header = f"第 {message_index} 条\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
    
    # 构建推送消息模板（优化格式）
    message = (
        f"{header}"
        f"💡 <b>推荐理由</b>：{tweet_data['recommendation_reason']}\n\n"
        f"📝 <b>推文内容</b>\n{tweet_data['username']} {tweet_data['author_id']} {tweet_data['time_since_published']}前\n\n"
        f"<i>{tweet_data['tweet_text']}</i>\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    )
    
    # 发送消息到Telegram
    try:
        bot = telegram.Bot(token=telegram_bot_token)
        
        # 使用asyncio运行异步函数
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        async def send_message():
            await bot.send_message(
                chat_id=channel_id,
                text=message,
                parse_mode='HTML',
                disable_web_page_preview=True
            )
        
        loop.run_until_complete(send_message())
        loop.close()
        
        print(f"✅ Alpha信息已成功推送到Telegram群组")
        
    except Exception as e:
        print(f"❌ 推送到Telegram失败: {str(e)}")
        raise

def push_all_alpha_tweets(recommended_tweets_array):
    """
    批量推送所有推荐的Alpha推文
    
    参数:
        recommended_tweets_array: 包含多个推荐推文的数组
    """
    if not recommended_tweets_array:
        print("📭 没有发现Alpha信息，无需推送")
        return
    
    total_count = len(recommended_tweets_array)
    print(f"📢 发现 {total_count} 条Alpha信息，开始推送...")
    
    for i, tweet_data in enumerate(recommended_tweets_array, 1):
        try:
            print(f"📤 正在推送第 {i}/{total_count} 条Alpha信息...")
            push_alpha_to_telegram(tweet_data, message_index=i, total_count=total_count)
            
            # 如果有多条消息，添加短暂延迟避免频率限制
            if i < total_count:
                import time
                time.sleep(0.5)  # 延迟0.5秒
                
        except Exception as e:
            print(f"❌ 推送第 {i} 条Alpha信息失败: {str(e)}")
            continue
    
    print(f"🎉 Alpha信息推送完成！")

# 示例用法
if __name__ == "__main__":
    # 测试数据
    test_tweet = {
        "recommendation_reason": "套利、撸毛、MEV（最大可提取价值）",
        "username": "秋田散人",
        "author_id": "@lnkybtc",
        "time_since_published": "17小时",
        "tweet_text": "讲一些关于套利的逻辑。\n对于圈内人，可以思考一下为什么一方cex刚上币的时候，或者跨链桥刚建立资产映射的时候，或多或少都有一些财富效应。\n实质是因为对于同一个东西的定价，在完全不同、或者尚未充分连接的两个经济系统内是有极大出入的。"
    }
    
    # 测试单条推送
    push_alpha_to_telegram(test_tweet)
    
    # 测试批量推送
    # push_all_alpha_tweets([test_tweet])