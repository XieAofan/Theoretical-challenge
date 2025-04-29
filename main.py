import WebSpider
import DBControl
import mainlib
import json
import time
import requests

# 条件检查函数
def check_condition(priority, db:DBControl.DB):
    result = db.get_question(time=db.timestamp_to_date(time.time()))

    if priority == 1:
        return True

    if result == None:
        return False
    
    for i in result:
        if i[3] >= 21 or i[4] < 10:
            return False
    return True

# 生成报告函数
def gen_report(db:DBControl.DB):
    text = db.timestamp_to_date(time.time()) + '\n'
    result = db.get_question(time=db.timestamp_to_date(time.time()))
    for i in result:
        text = text + f"{i[2]}\t{i[3]}\t{i[4]}\n"
    return text

# 发送消息函数
def send_message(content, summary, content_type, spt=None, spt_list=None, url=None):
    """
    使用WxPusher发送消息

    Args:
        content (str): 推送内容
        summary (str): 消息摘要（可选）
        content_type (int): 内容类型（1: 文字, 2: HTML, 3: Markdown）
        spt (str): 单个用户的SPT（可选）
        spt_list (list): 多个用户的SPT列表（可选）
        url (str): 原文链接（可选）

    Returns:
        dict: API响应结果
    """
    url = "https://wxpusher.zjiecode.com/api/send/message/simple-push"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "content": content,
        "summary": summary,
        "contentType": content_type
    }
    
    if spt:
        data["spt"] = spt
    if spt_list:
        data["sptList"] = spt_list
    if url:
        data["url"] = url
    
    response = requests.post(url, headers=headers, json=data)
    return response.json()

if __name__ == '__main__':
    # 初始化
    db = DBControl.DB()
    db.init()
    message = '运行成功'

    # 读取配置文件
    with open("setting.json", "r") as f:
        rd = f.read()
    setting_list = json.loads(rd)
    
    # 优先级排序
    user_List = setting_list['userList']
    user_List.sort(key=lambda x: x['priority'])

    for user_setting in user_List:
        # 检查状态
        if not user_setting['status']:
            print("用户状态为关闭，跳过该用户")
            
            continue

        # 检查条件是否满足
        if not check_condition(user_setting['priority'], db):
            print("条件不满足，跳过该用户")
            message = f"用户{user_setting['userName']}运行出错，条件不满足"
            continue
        
        # 答题逻辑
        try:
            mainlib.run_user(user_setting['userName'], user_setting['password'], db, user_setting['TimeLimit'])
        except Exception as e:
            message = f"用户{user_setting['userName']}运行出错，错误信息为：{e}"
            print(e)
    
    report = gen_report(db)
    if message == '运行成功':
        print("运行成功")
        # 发送报告消息
        send_message(
            content=report,
            summary="答题报告",
            content_type=1,
            spt="SPT_2CH4KczNN6QwbzkVo4a1T05TX0f6"  # 替换为实际的SPT
        )
    else:
        send_message(
            content=message,
            summary="运行失败",
            content_type=1,
            spt="SPT_2CH4KczNN6QwbzkVo4a1T05TX0f6"  # 替换为实际的SPT
        )
    db.close()