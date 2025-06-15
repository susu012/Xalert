# 导入必要的库
import time
from DrissionPage import Chromium
from DrissionPage import ChromiumOptions
import os
from dotenv import load_dotenv
import datetime

def get_browser():
    """
    配置并启动浏览器。
    使用用户数据路径以保持登录状态，并设置窗口大小。
    """
    # 设置Chrome用户数据路径，如果你已经在这个路径下登录过X.com，
    # 浏览器会保持登录状态，这样就能访问到你的个性化推文。
    # 建议先手动启动一次浏览器，登录X.com并保持登录，然后关闭浏览器。
    option = ChromiumOptions().set_paths(user_data_path=r'./chrome_data',local_port=int(os.getenv('chrome_debug_port', 9777)))
    
    # 设置启动时窗口大小，以便观察抓取过程。
    # 如果想在后台运行，可以取消注释 option = option.headless()
    option = option.set_argument('--window-size', '2000,1500')
    
    # 启动或接管浏览器，并创建标签页对象
    chrome = Chromium(addr_or_opts=option)
    
    # 设置页面操作的默认超时时间，给页面加载留出足够的时间
    chrome.set.timeouts(30) # 增加超时时间，以应对网络延迟或动态内容加载
    
    # 获取最新的标签页
    tab1 = chrome.latest_tab
    
    # 访问X.com主页
    tab1.get(r"https://x.com/")
    
    print("浏览器已启动并尝试访问 X.com。")
    return chrome

def get_twitter_information(scroll_count=3, scroll_pause_time=3):
    """
    获取推特动态加载的推文内容。
    模拟滚动行为以加载更多推文，并提取可见推文的文本。

    Args:
        browser: DrissionPage Chromium 实例。
        scroll_count (int): 向下滚动的次数。每次滚动会尝试加载更多推文。
        scroll_pause_time (int): 每次滚动后暂停的秒数，用于等待新内容加载。

    Returns:
        str: 提取到的所有独特推文内容，以 --- 分隔。
    """
    browser = get_browser()
    tab1 = browser.latest_tab
    tweets_data = [] # 存储抓取到的推文文本
    seen_tweet_texts = set() # 使用集合来去重，避免重复抓取相同的推文

    print(f"开始获取推文内容。将向下滚动 {scroll_count} 次，每次滚动后暂停 {scroll_pause_time} 秒。")

    # 初始等待，确保页面主要结构加载完成，特别是对于首次访问X.com
    time.sleep(7)
    
    # 首先抓取初始页面的推文（这是最重要的部分！）
    print("正在抓取初始页面的推文...")
    initial_tweet_elements = tab1.eles('xpath://article[@data-testid="tweet"]')
    
    if initial_tweet_elements:
        for tweet_ele in initial_tweet_elements:
            tweet_text = tweet_ele.text.strip()
            if tweet_text and tweet_text not in seen_tweet_texts:
                seen_tweet_texts.add(tweet_text)
                tweets_data.append(tweet_text)
        print(f"初始页面抓取到 {len(tweets_data)} 条推文。")
    else:
        print("警告：初始页面未找到推文元素。")

    for i in range(scroll_count):
        print(f"第 {i+1}/{scroll_count} 次向下滚动...")
        # 模拟向下滚动，加载更多内容
        # 滚动5000像素，这个值可能需要根据你的屏幕大小和推文密度调整
        tab1.scroll.down(5000)
        
        # 暂停一段时间，等待新内容加载和渲染到DOM中
        time.sleep(scroll_pause_time)

        # 查找所有推文元素。X.com的推文通常在 <article data-testid="tweet"> 标签中。
        # 这个XPath选择器在大多数情况下是稳定的，但如果X.com更新UI，可能需要根据新的HTML结构进行调整。
        tweet_elements = tab1.eles('xpath://article[@data-testid="tweet"]')

        if not tweet_elements:
            print("警告：未找到推文元素。请检查网络连接，或更新推文选择器。")
            # 如果找不到推文，可能是页面未加载、选择器错误或已达页面底部，停止滚动。
            break

        current_scroll_new_tweets_count = 0
        for tweet_ele in tweet_elements:
            # 尝试获取推文元素的可见文本内容。
            # DrissionPage的.text属性通常会返回元素及其所有子元素的可见文本，
            # 并且会去除HTML标签，只保留纯文本。
            tweet_text = tweet_ele.text.strip()

            # 检查文本是否为空，并且是否已经抓取过这条推文
            if tweet_text and tweet_text not in seen_tweet_texts:
                seen_tweet_texts.add(tweet_text)
                tweets_data.append(tweet_text)
                current_scroll_new_tweets_count += 1
                # 可以在这里打印每条新抓取到的推文，用于调试
                # print(f"--- 抓取到新推文 ---\n{tweet_text}\n--------------------")

        print(f"本轮滚动新增 {current_scroll_new_tweets_count} 条推文。当前共抓取 {len(tweets_data)} 条独特推文。")
        
        # 优化：如果某一轮滚动没有新增推文，且不是第一次滚动，可能已经到达页面底部或者没有更多内容了，停止。
        if current_scroll_new_tweets_count == 0 and i > 0:
             print("本轮未发现新推文，可能已达页面底部或无更多内容。停止滚动。")
             break

    print(f"\n抓取完成。总共获取到 {len(tweets_data)} 条独特推文。")
    
    # 将所有推文内容用Markdown的分隔符 (---) 连接起来，便于后续处理。
    result = "\n---\n".join(tweets_data)
    
    # 保存到文件
    save_tweets_to_file(result)
    
    return result

def save_tweets_to_file(content):
    """
    将推文内容保存到按日期分层的txt文件中
    
    文件结构：
    tweets/
    ├── 2024-01-15/
    │   ├── 1430.txt
    │   ├── 1435.txt
    │   └── 1440.txt
    ├── 2024-01-16/
    │   ├── 0900.txt
    │   └── 0905.txt
    
    Args:
        content (str): 格式化后的推文内容
    """
    now = datetime.datetime.now()
    
    # 创建日期文件夹：YYYY-MM-DD格式
    date_folder = now.strftime('%Y-%m-%d')
    dir_path = os.path.join('./tweets', date_folder)
    
    # 确保目录存在
    os.makedirs(dir_path, exist_ok=True)
    
    # 文件名：HHMM.txt格式（如：1430.txt表示14:30抓取的数据）
    filename = f"{now.strftime('%H%M')}.txt"
    filepath = os.path.join(dir_path, filename)
    
    # 准备文件内容：添加时间戳头部信息
    file_content = f"抓取时间: {now.strftime('%Y-%m-%d %H:%M:%S')}\n"
    file_content += f"Unix时间戳: {int(now.timestamp())}\n"
    file_content += "=" * 50 + "\n\n"
    file_content += content
    
    # 保存txt文件
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(file_content)
    
    print(f"推文已保存到: {filepath}")

if __name__ == '__main__':
    try:
        get_browser()
    except Exception as e:
        print(f"发生错误: {e}")