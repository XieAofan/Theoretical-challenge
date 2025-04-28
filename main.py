import WebSpider
import DBControl
import mainlib
import json
import time

# 条件检查函数
def check_condition(priority, db:DBControl.DB):
    result = db.get_question(time=db.timestamp_to_date(time.time()))

    if priority == 1:
        return True
    
    for i in result:
        if i['priority'] < priority:
            if i['duration'] > 20 or i['score'] < 10:
                return False
    return True

if __name__ == '__main__':
    # 初始化
    db = DBControl.DB()

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
            continue
        
        # 答题逻辑
        try:
            mainlib.run_user(user_setting['username'], user_setting['password'], db, user_setting['waitTime'])
        except Exception as e:
            print(e)

