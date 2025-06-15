from google import genai
import os
from dotenv import load_dotenv

def get_ai_analysis(prompt):
    print("🤖开始对推文进行分析：")
    load_dotenv()  # 从 .env 文件加载环境变量
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("环境变量里没有API_KEY字段")

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(model="gemini-2.5-flash-preview-05-20", contents=prompt)
    return response.text

def get_this_project_ai_analysis(twitter_content):
    
    # 读取项目根目录下的prompt.txt文件
    try:
        with open('prompt.txt', 'r', encoding='utf-8') as f:
            twitter_analysis_prompt = f.read()
        
        # 将推文内容添加到提示词末尾
        twitter_analysis_prompt += f"\n\n{twitter_content}"
        
    except FileNotFoundError:
        raise FileNotFoundError("找不到prompt.txt文件，请确保文件存在于项目根目录")
    except Exception as e:
        raise Exception(f"读取prompt.txt文件时出错：{str(e)}")
    
    ai_result = get_ai_analysis(twitter_analysis_prompt)
    
    # 清理AI返回内容中的markdown代码块标记
    if ai_result.startswith('```json'):
        # 移除开头的```json
        ai_result = ai_result[7:]
    if ai_result.endswith('```'):
        # 移除结尾的```
        ai_result = ai_result[:-3]
    
    # 去除首尾空白字符
    ai_result = ai_result.strip()
    
    #返回值是一个json
    return ai_result