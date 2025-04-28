import WebSpider
import DBControl
import os
import time

def run_user(username, password, db:DBControl.DB, wt=20):
    # 初始化
    dir = os.path.join(os.getcwd(), 'data', username)
    web = WebSpider.Web(dir, db, username, password)
    web.get_cookie()

    # print(f"Now Cookie is {web.cookie['JSESSIONID']}")
    web.log(f"Now Cookie is {web.cookie['JSESSIONID']}")
    print(f"当前用户名{web.username}")
    web.log(f"当前用户名{web.username}")

    # 登陆
    if web.is_login() == False:
        web.login(username, password)
    if web.is_login() == False:
        return False
    web.save_cookie()

    # 答题逻辑
    times = 1  # 定义答题计数
    while times < 2:
        
        # a = input("Press Enter to continue...")
        try:
            answer_question(web, wt)

        except WebSpider.SubTimeError as e:
            print(e)
            web.log(e)
            continue

        times += 1
        time.sleep(1)

def answer_question(web:WebSpider.Web, wt=20):
    # 初始化
    web.jf = 'Error'

    web.get_roomid()
    web.get_roompage()

    ts = time.time()
    testid = web.get_testid()
    html = web.get_review()
    question_List = web.get_ans(html)

    i = 0
    for q in question_List:
        i += 1
        time.sleep(1)
        print(f"{i}/10")
        web.submit_ans(q[2], q[3], q[1])
        tn = time.time()
        if i == 10:
            tes = time.time() # 记录开始等待前的时间戳
            if tn-ts < wt:
                print("Waiting...")
                tn = time.time()
                time.sleep(wt-(tn-ts)-.1)
        web.get_result(i+1)
    te = time.time()

    # log
    print(f'SleepedTimeUsed: {tes-ts}')
    web.log(f'SleepedTimeUsed: {tes-ts}')
    print(f'TimeUsed: {te-ts}')
    web.log(f'TimeUsed: {te-ts}')
    web.db.add(username=web.username, duration=te-ts, score=web.jf)