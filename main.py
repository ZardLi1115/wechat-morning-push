import time
import requests
import json
import schedule
from bs4 import BeautifulSoup

# 导入配置文件
from config import (appID, appSecret, openIds, weather_template_id, city1, city2,
                    SENIVERSE_API_KEY, SENIVERSE_API_HOST,
                    SENIVERSE_WEATHER_URL, SENIVERSE_DAILY_URL,
                    MINIMAX_API_KEY, MINIMAX_API_HOST, MINIMAX_CHAT_URL, MINIMAX_MODEL)


def get_weather(my_city):
    """
    使用心知天气API获取城市天气信息
    返回: (城市名, 气候, 最低温度, 最高温度, 当前温度)
    """
    try:
        # 1. 获取实时天气（用于获取当前温度和气候）
        current_url = f"{SENIVERSE_API_HOST}{SENIVERSE_WEATHER_URL}"
        current_params = {
            "location": my_city,
            "key": SENIVERSE_API_KEY,
            "language": "zh-Hans",  # 简体中文
            "unit": "c"  # 摄氏度
        }
        print(f"正在获取 {my_city} 的实时天气...")
        print(f"URL: {current_url}")
        print(f"Params: {current_params}")
        current_response = requests.get(current_url, params=current_params, timeout=10)
        print(f"实时天气状态码: {current_response.status_code}")
        
        if current_response.status_code != 200:
            print(f"获取实时天气失败: {current_response.text[:200]}")
            return None
            
        current_data = current_response.json()
        print(f"实时天气响应: {current_data}")
        
        # 检查是否有结果
        if "results" not in current_data or len(current_data["results"]) == 0:
            print(f"实时天气API错误: {current_data}")
            return None
        
        # 2. 获取3天天气预报（用于获取最高/最低温度）
        daily_url = f"{SENIVERSE_API_HOST}{SENIVERSE_DAILY_URL}"
        daily_params = {
            "location": my_city,
            "key": SENIVERSE_API_KEY,
            "language": "zh-Hans",
            "unit": "c",
            "start": 0,  # 从今天开始
            "days": 3    # 获取3天
        }
        print(f"正在获取 {my_city} 的预报天气...")
        daily_response = requests.get(daily_url, params=daily_params, timeout=10)
        print(f"预报天气状态码: {daily_response.status_code}")
        
        if daily_response.status_code != 200:
            print(f"获取预报天气失败: {daily_response.text[:200]}")
            return None
            
        daily_data = daily_response.json()
        print(f"预报天气响应: {daily_data}")
        
        if "results" not in daily_data or len(daily_data["results"]) == 0:
            print(f"预报天气API错误: {daily_data}")
            return None
        
        # 解析实时天气
        now = current_data["results"][0]["now"]
        current_temp = now["temperature"]  # 当前温度
        climate = now["text"]  # 天气状况（晴、多云等）
        
        # 解析今日预报（获取最高/最低温度）
        today_forecast = daily_data["results"][0]["daily"][0]
        min_temp = today_forecast["low"]  # 最低温度
        max_temp = today_forecast["high"]  # 最高温度
        
        print(f"{my_city} 天气: {climate}, 当前{current_temp}°, 范围{min_temp}°-{max_temp}°")
        return my_city, climate, min_temp, max_temp, current_temp
            
    except Exception as e:
        print(f"请求天气API出错: {e}")
        import traceback
        traceback.print_exc()
        return None


def get_access_token():
    # 获取access token的url
    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}' \
        .format(appID.strip(), appSecret.strip())
    response = requests.get(url).json()
    print(response)
    access_token = response.get('access_token')
    return access_token


def get_daily_love():
    """
    使用Minimax M2.5模型生成每日中文情话 (Anthropic API兼容方式)
    """
    url = f"{MINIMAX_API_HOST}{MINIMAX_CHAT_URL}"

    headers = {
        "Content-Type": "application/json",
        "x-api-key": MINIMAX_API_KEY,  # Anthropic兼容方式使用x-api-key
        "anthropic-version": "2023-06-01"  # Anthropic API版本
    }

    # 检查API Key是否已设置
    if MINIMAX_API_KEY == "YOUR_MINIMAX_API_KEY":
        print("警告: Minimax API Key 未设置，使用默认情话")
        return "每一天都在期待与你相见。"

    # 构建提示词，要求生成类似风格的中文情话
    prompt = """请生成一句浪漫的中文情话，要求：
1. 简洁优美，带有期待和思念的情感
2. 不要包含对方的名字
3. 可以提及宽泛的地点或场景，营造画面感，但不要有具体的地名
5. 字数控制在15字以内
6. 只返回情话内容，不要有任何解释或前缀
"""

    # Anthropic兼容格式的payload
    payload = {
        "model": MINIMAX_MODEL,
        "max_tokens": 500,
        "system": "你是一个浪漫的情话生成器，擅长用简洁优美的中文表达深情。",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ],
        "thinking": {
            "type": "disabled"  # 禁用thinking模式，直接返回结果
        }
    }

    try:
        print("正在使用Minimax生成情话...")
        print(f"URL: {url}")
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        print(f"Minimax API状态码: {response.status_code}")

        if response.status_code != 200:
            print(f"Minimax API请求失败: {response.text[:200]}")
            # 如果API失败，返回默认情话
            return "每一天都在期待与你相见。"

        data = response.json()
        print(f"Minimax响应: {data}")

        # 解析Anthropic兼容格式的响应
        if "content" in data and len(data["content"]) > 0:
            # 遍历content数组，找到text类型的内容
            for block in data["content"]:
                if block.get("type") == "text":
                    love_sentence = block.get("text", "").strip()
                    # 移除可能的引号
                    love_sentence = love_sentence.strip('"').strip("'")
                    print(f"生成的情话: {love_sentence}")
                    return love_sentence
            # 如果没有找到text类型，返回默认
            return "每一天都在期待与你相见。"
        else:
            print(f"无法解析Minimax响应: {data}")
            return "每一天都在期待与你相见。"

    except Exception as e:
        print(f"调用Minimax API出错: {e}")
        import traceback
        traceback.print_exc()
        # 返回默认情话
        return "每一天都在期待与你相见。"


def calculate_days():
    """
    计算日期相关
    date1: 从2026年1月1日到今天过了多少天
    date2: 从今天到2026年3月3日还要过多少天
    """
    import datetime
    today = datetime.date.today()
    
    # 2026年1月1日
    start_date = datetime.date(2026, 1, 1)
    # 2026年3月3日
    target_date = datetime.date(2026, 3, 3)
    
    # 从2026年1月1日到今天过了多少天
    days_from_start = (today - start_date).days
    
    # 从今天到2026年3月3日还要过多少天
    days_to_target = (target_date - today).days
    
    return days_from_start, days_to_target


def build_weather_body(access_token, weather1, weather2):
    """
    构建天气消息body并发送给所有收信人
    weather1: 城市1的天气数据 (城市名, 气候, 最低温度, 最高温度, 当前温度)
    weather2: 城市2的天气数据 (城市名, 气候, 最低温度, 最高温度, 当前温度)
    """
    import datetime
    today = datetime.date.today()
    today_str = today.strftime("%Y年%m月%d日")

    # 计算日期
    days_from_start, days_to_target = calculate_days()

    # 获取情话（只生成一次，所有收信人使用相同的情话）
    love_sentence = get_daily_love()

    # 构建消息体模板（不包含touser）
    body_template = {
        "template_id": weather_template_id.strip(),
        "url": "https://weixin.qq.com",
        "data": {
            "date": {
                "value": today_str
            },
            "city1": {
                "value": weather1[0]
            },
            "climate1": {
                "value": weather1[1]
            },
            "temp_a_1": {
                "value": weather1[2]
            },
            "temp_a_2": {
                "value": weather1[3]
            },
            "temp_cur_1": {
                "value": weather1[4]
            },
            "city2": {
                "value": weather2[0]
            },
            "climate2": {
                "value": weather2[1]
            },
            "temp_b_1": {
                "value": weather2[2]
            },
            "temp_b_2": {
                "value": weather2[3]
            },
            "temp_cur_2": {
                "value": weather2[4]
            },
            "date1": {
                "value": str(days_from_start)
            },
            "date2": {
                "value": str(days_to_target)
            },
            "love_sentence": {
                "value": love_sentence
            }
        }
    }

    url = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}'.format(access_token)

    # 向每个收信人发送消息
    results = []
    for open_id in openIds:
        body = body_template.copy()
        body["touser"] = open_id.strip()

        print(f"正在发送消息给: {open_id}")
        response = requests.post(url, json.dumps(body))
        print(f"发送结果: {response.text}")
        results.append({
            "open_id": open_id,
            "response": response.json()
        })

    return results



def weather_report(city1, city2):
    """
    获取两个城市的天气并发送消息
    city1: 城市1名称（如：桂林）
    city2: 城市2名称（如：台州）
    """
    # 1.获取access_token
    access_token = get_access_token()
    # 2. 获取两个城市的天气
    weather1 = get_weather(city1)
    weather2 = get_weather(city2)
    print(f"城市1天气信息： {weather1}")
    print(f"城市2天气信息： {weather2}")
    # 3. 发送消息
    if weather1 and weather2:
        build_weather_body(access_token, weather1, weather2)
    else:
        print("获取天气信息失败")


def timetable(message):
    # 1.获取access_token
    access_token = get_access_token()
    # 3. 发送消息
    send_timetable(access_token, message)


if __name__ == '__main__':
    # 发送配置文件中两个城市的天气
    weather_report(city1, city2)
