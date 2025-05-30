# Theoretical Challenge 自动答题系统

## 简介
Theoretical Challenge 自动答题系统是一个用于自动完成在线答题任务的Python项目。该系统能够自动登录答题网站，获取题目，提交答案，并记录答题结果。

## 功能
- 自动登录答题网站
- 获取答题房间信息
- 解析题目并提交答案
- 记录答题结果到本地数据库
- 生成答题报告并通过WxPusher发送消息

## 安装
1. 确保你已经安装了Python 3.x。
2. 安装所需的Python库：
   ```bash
   pip install requests beautifulsoup4
   ```
3. 克隆项目到本地：
   ```bash
   git clone https://github.com/your-repo/Theoretical-challenge.git
   cd Theoretical-challenge
   ```

## 使用
1. 配置`setting.json`文件，添加用户信息和答题设置。
2. 运行`main.py`：
   ```bash
   python main.py
   ```

## 配置文件说明
`setting.json`文件示例：
```json
{
    "userList": [
        {
            "userName": "your_username",
            "password": "your_password",
            "status": true,
            "priority": 1,
            "TimeLimit": 20
        }
    ]
}
```

## 数据库
项目使用SQLite数据库存储答题记录。数据库文件为`data.db`，表结构如下：
- `question`表：存储答题记录，包括时间、用户名、答题时长和得分。

## 日志
系统会将运行日志记录在每个用户的日志文件中，路径为`data/username/log.txt`。

## 贡献
欢迎任何形式的贡献！请参考[贡献指南](CONTRIBUTING.md)。

## 许可证
本项目采用MIT许可证。详情请参考[LICENSE](LICENSE)文件。
