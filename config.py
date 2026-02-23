# 微信公众号配置
# 从测试号信息获取: https://mp.weixin.qq.com/debug/cgi-bin/sandbox?t=sandbox/login

# 微信 AppID
appID = "YOUR-APPID"

# 微信 AppSecret
appSecret = "YOUR-APPSECRET"

# 收信人ID (用户列表中的微信号)
# 支持多个收信人，用列表存储//单收信人直接赋值即可
openIds = [
    "YOUR-OPENID-1",
    "YOUR-OPENID-2"
]

# 天气预报模板ID
weather_template_id = "YOUR-TEMPLATE-ID"

# 城市配置
city1 = "YOUR-CITY1"  # 第一个城市
city2 = "YOUR-CITY2"  # 第二个城市


# ==================== 心知天气 API 配置 ====================
# 心知天气开发平台: https://www.seniverse.com/
# 请在这里填写你的心知天气 API Key
SENIVERSE_API_KEY = "YOUR-SENIVERSE-API-KEY"

# 心知天气 API 基础地址
SENIVERSE_API_HOST = "https://api.seniverse.com"

# 心知天气 API 路径
# 实况天气 API
SENIVERSE_WEATHER_URL = "/v3/weather/now.json"
# 每日天气预报 API
SENIVERSE_DAILY_URL = "/v3/weather/daily.json"


# ==================== Minimax API 配置 ====================
# Minimax 开发平台: https://platform.minimaxi.com/
# 请在这里填写你的 Minimax API Key
MINIMAX_API_KEY = "YOUR-MINIMAX-API-KEY"

# Minimax API 基础地址 (Anthropic 兼容方式)
MINIMAX_API_HOST = "https://api.minimaxi.com/anthropic"

# Minimax M2.5 模型 API 路径 (Anthropic 兼容方式)
MINIMAX_CHAT_URL = "/v1/messages"

# 使用的模型名称
MINIMAX_MODEL = "MiniMax-M2.5"
