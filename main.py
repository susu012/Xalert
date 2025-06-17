import browser
import ai
import push
import json

def main_progress():
    #所有的必备数据存储在环境变量中，包括AI的API
    #调用浏览器访问网页
    #获取网页内容，按获取的日期-时分秒-时间戳保存到本地的tweets文件夹中
    #遍历tweets文件夹，找到最新时间戳的推文（这个让AI想想有没有更佳实践，遍历文件名感觉挺蠢的）
    #按照.env中设定的deepseek或gemini，调用deepseek或gemini的API，让AI分析这次这次浏览网页的文章
    #AI的提示词保存在项目根目录下的prompt.txt文件中
    #让AI返回一个json，有两个字段，第一个字段是has_alpha，如果是True就是有alpha，是Flase就是没有alpha
    #第二个字段是reason，是一个字符串，说明AI的判断理由
    #第三个字段是受到AI推荐的原始推文，字段名为recommend_tweet

    all_tweets_in_markdown = browser.get_twitter_information()

    #构造"prompt.txt+推文"字符串，传入到ai分析的函数，获得json
    ai_response = ai.get_this_project_ai_analysis(all_tweets_in_markdown)

    # 解析AI返回的JSON数据
    try:
        # 如果AI返回的是字符串格式的JSON，需要解析
        if isinstance(ai_response, str):
            ai_json = json.loads(ai_response)
        else:
            ai_json = ai_response
        
        # 获取推荐的推文数组
        recommended_tweets = ai_json.get('recommended_tweets', [])
        
        print(f"🔍 AI分析完成，发现 {len(recommended_tweets)} 条Alpha信息")
        
        # 循环json调用推送函数，推送到telegram
        if recommended_tweets:
            push.push_all_alpha_tweets_combined(recommended_tweets)
        else:
            print("📭 本次分析未发现Alpha信息，无需推送")
            
    except json.JSONDecodeError as e:
        print(f"❌ 解析AI返回的JSON数据失败: {str(e)}")
        print(f"AI原始返回内容: {ai_response}")
    except Exception as e:
        print(f"❌ 处理推送逻辑时出错: {str(e)}")

    #再写一个sh脚本，用来保证
    #再写一个脚本，只调用browser.py中的get_browser函数，按任意键退出，用来配置推特账号
    #然后试运行一下，去干买一价和卖一价问题，我打算先把调试信息给获取出来，因为我怀疑是获取了错误的字段，这得看清楚这个函数是怎么运行的

if __name__ == '__main__':
    main_progress()