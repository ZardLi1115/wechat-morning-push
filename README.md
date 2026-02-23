# 💕 微信早安推送

一个基于 Python 的微信公众号早安推送程序，每天自动给指定用户发送天气信息和浪漫情话。

## ✨ 功能特点

- 🌤 **双城市天气推送** - 同时获取两个城市的天气信息
- 🤖 **AI 情话生成** - 使用 Minimax M2.5 模型自动生成每日浪漫情话
- 📅 **恋爱纪念日** - 自动计算恋爱天数和重逢倒计时
- ⏰ **定时推送** - 支持定时自动发送（可配合云服务器或 GitHub Actions）

## 📝 消息模板示例

```
现在是2026年2月23日早上8点
今日桂林晴，温度12°~20°,目前气温15°;
今日台州多云，温度10°~18°,目前气温14°
这是我们恋爱的第54天，距离我们在杭州重逢还有8天
小公主 每一天都在期待与你相见。
```

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置参数

编辑 `config.py` 文件，填写以下信息：

```python
# 微信公众号配置（从测试号获取）
appID = "your-app-id"
appSecret = "your-app-secret"
openIds = ["user-open-id"]  # 收信人列表
weather_template_id = "your-template-id"

# 城市配置
city1 = "桂林"  # 第一个城市
city2 = "台州"  # 第二个城市

# API 密钥
SENIVERSE_API_KEY = "your-seniverse-api-key"      # 心知天气
MINIMAX_API_KEY = "your-minimax-api-key"          # Minimax AI
```

### 4. 配置微信模板

在微信公众号后台创建模板消息，内容格式参考 `模板.txt`：

```
现在是{{date.DATA}}早上8点
今日{{city1.DATA}}{{climate1.DATA}}，温度{{temp_a_1.DATA}}~{{temp_a_2.DATA}},目前气温{{temp_cur_1.DATA}};
今日{{city2.DATA}}{{climate2.DATA}}，温度{{temp_b_1.DATA}}~{{temp_b_2.DATA}},目前气温{{temp_cur_2.DATA}}
这是我们恋爱的第{{date1.DATA}}天，距离我们在杭州重逢还有{{date2.DATA}}天
小公主{{love_sentence.DATA}}
```

### 5. 运行程序

```bash
python main.py
```

## 🔧 配置说明

### 微信公众号（测试号）

1. 访问 [微信公众平台测试号](https://mp.weixin.qq.com/debug/cgi-bin/sandbox?t=sandbox/login)
2. 扫码登录后获取 `appID` 和 `appsecret`
3. 扫描测试号二维码关注，获取用户 `openid`
4. 在「模板消息接口」中创建模板，获取 `模板ID`

### 心知天气 API

1. 注册 [心知天气](https://www.seniverse.com/)
2. 创建应用获取 API Key
3. 免费版支持每日 400 次调用

### Minimax AI

1. 注册 [Minimax 开放平台](https://platform.minimaxi.com/)
2. 创建应用获取 API Key
3. 用于生成每日浪漫情话

## 📁 项目结构

```
.
├── main.py           # 主程序
├── config.py         # 配置文件
├── requirements.txt  # 依赖列表
├── 模板.txt          # 微信模板格式参考
└── README.md         # 项目说明
```

## ⏰ 定时推送方案

### 方案一：云服务器 + crontab

```bash
# 编辑 crontab
crontab -e

# 每天早上 8 点执行
0 8 * * * cd /path/to/project && /usr/bin/python3 main.py
```

### 方案二：GitHub Actions

创建 `.github/workflows/schedule.yml` 文件实现定时推送。

## 🛠 技术栈

- **Python 3.10+**
- **requests** - HTTP 请求
- **schedule** - 定时任务
- **BeautifulSoup** - HTML 解析
- **心知天气 API** - 天气数据
- **Minimax M2.5** - AI 情话生成

## ⚠️ 注意事项

1. **隐私安全**：`config.py` 包含敏感信息
2. **API 限制**：免费版 API 有调用次数限制，请注意使用频率
3. **日期配置**：恋爱起始日和重逢日需要在 `main.py` 中修改：
   ```python
   start_date = datetime.date(2026, 1, 1)  # 恋爱开始日期
   target_date = datetime.date(2026, 3, 3)  # 重逢日期
   ```

## 📄 License

MIT License

## 💝 致谢

- 心知天气提供天气数据服务
- Minimax 提供 AI 生成服务

---

Made with 💕 for someone special
