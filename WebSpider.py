import requests
import re
from bs4 import BeautifulSoup
import json
import time
from urllib.parse import urlencode
import random
import os
# import pandas as pd
import DBControl

class SubTimeError(Exception):
    """答题时间异常"""
    def __init__(self, message="答题时间异常"):
        super().__init__(message)

class SubAnswerError(Exception):
    """自定义异常类"""
    def __init__(self, message="上报异常异常"):
        super().__init__(message)


class Web:
    def __init__(self, data_dir, db, username=None, password=None):
        self.cookie = None
        self.roomid = None
        self.paperid = None
        self.get_username = None
        self.username = username
        self.password = password
        self.versionId = 1
        self.testid = 1
        self.loginUserId = 1
        self.db = db
        self.db.init()
        
        app_folder = data_dir
        # 如果目录不存在，则创建
        if not os.path.exists(app_folder):
            os.makedirs(app_folder)
        self.app_folder = app_folder
        self.headers = {
            "User-Agent": "Mozilla/5.0+(Linux;+Android+10;+ELE-AL00+Build/HUAWEIELE-AL00;+wv)+AppleWebKit/537.36+(KHTML,+like+Gecko)+Version/4.0+Chrome/78.0.3904.62+XWEB/2691+MMWEBSDK/200901+Mobile+Safari/537.36+MMWEBID/215+MicroMessenger/7.0.19.1760(0x2700133F)+Process/toolsmp+WeChat/arm64+NetType/WIFI+Language/zh_CN+ABI/arm64"
        }
        path = os.path.join(self.app_folder, 'log.txt')
        self.f = open(path, 'a', encoding='utf-8')
        #self.c = open('cookie.txt', 'a', encoding='utf-8')
    
    def get_cookie(self, path="cookie.json"):
        path = os.path.join(self.app_folder, path)
        if self.cookie == None:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    d = json.load(f)
                    self.cookie = d['cookie']
                    
            except:
                f = open(path, 'w', encoding='utf-8')
                self.cookie = {'JSESSIONID': 'XXXXXXXXXXXXXXXXXXXXXXX'}
                
        return self.cookie
    
    def save_cookie(self, path='cookie.json'):
        path = os.path.join(self.app_folder, path)
        d = {
            "cookie":self.cookie,
        }
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(d, f)
        except:
            raise Warning('cookie error')
        return 0

    def log(self, text):
        try:
            formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            self.f.write(f"[{formatted_time}] {text}\n")
        except:
            raise Warning('log error')
        return 0

    def is_login(self):
        url = 'http://mapp.nudt.edu.cn/home/index.do'
        be = requests.get(url, headers=self.headers, cookies=self.cookie)
        text = be.text
        pattern = r'<div class="userinfo">\s*(\w+)\s*欢迎回来\s*</div>'
        match = re.search(pattern, text)

        if match:
            username = match.group(1)
            self.get_username = username
            print("用户名是:", username)
            if self.username != None:
                if username != self.username:
                    self.log(f"用户名错误，请检查用户名是否正确，当前用户名：{username}")
                    print(f"用户名错误，请检查用户名是否正确，当前用户名：{username}")
                    return False
            self.username = username
            return True
        else:
            print("未找到用户名")
            # raise Warning('login error')
        return False
    
    def login(self, username, password):
        if self.get_username == username:
            return True
        self.username = username
        self.password = password
        url = 'http://mapp.nudt.edu.cn/login/webPage.do'
        be = requests.get(url, headers=self.headers, cookies=self.cookie)

        cookie = be.cookies
        cookie = cookie.items()

        if cookie == []:
            cookie = self.cookie
        else:
            cookie = dict(cookie)
            self.cookie = cookie
        
        post_data = {
            'uniqueIdentifier': '87bc417ebee29ea52e6cc4bd8d0baec1',
            'userAgent': 'Mozilla/5.0+(Linux;+Android+10;+ELE-AL00+Build/HUAWEIELE-AL00;+wv)+AppleWebKit/537.36+(KHTML,+like+Gecko)+Version/4.0+Chrome/78.0.3904.62+XWEB/2691+MMWEBSDK/200901+Mobile+Safari/537.36+MMWEBID/215+MicroMessenger/7.0.19.1760(0x2700133F)+Process/toolsmp+WeChat/arm64+NetType/WIFI+Language/zh_CN+ABI/arm64',
            'screenResolution':'390x844',
            'screenWidth':'390',
            'mobile':username,
            'name': username,
            'password': password,
            'isrememberMeId': 'on',
            'timeZone': 'Asia/Hong_Kong',
            'language': 'zh_CN',
            'webglRenderer': 'ANGLE (Intel, Intel(R) Arc(TM) Graphics (0x00007D55) Direct3D11 vs_5_0 ps_5_0, D3D11)'
        }

        url = 'http://mapp.nudt.edu.cn/login/websubmitapp.do'
        response = requests.post(url, data=post_data, cookies=cookie, headers=self.headers)
        # print(response.status_code)
        if response.cookies.items() != []:
            cookie = response.cookies
            cookie = cookie.items()
            cookie = dict(cookie)
            self.cookie = cookie
            print('Cookie:', self.cookie)
            self.log('Cookie:'+str(self.cookie))
        if response.status_code == 200:
            self.cookie = cookie
            print('Login successfully.')
            self.log('Login successfully.')
        else:
            raise Exception("Login failed.")
        
    def get_roomid(self):
        url = 'http://mapp.nudt.edu.cn/home/answerRoom.do'
        response = requests.get(url, cookies=self.cookie, headers=self.headers)
        text = response.text

        soup = BeautifulSoup(text, 'html.parser')
        button = soup.find('button', class_='loginbtn')
        # text2 = button.get('onclick')
        # print(text)
        match = re.search(r"submitRoomPage\('([^']+)','([^']+)'\)", text)
        type = match.groups()[0]
        roomid = match.groups()[1]
        self.roomid = roomid
        self.subjectType = type
        self.log(f"Room ID: {self.roomid}, Subject Type: {self.subjectType}")
        print(f"Room ID: {self.roomid}, Subject Type: {self.subjectType}")

    def get_roompage(self):
        url = 'http://mapp.nudt.edu.cn/exam/roompage.do'
        param = {
            'roomid': self.roomid,
            'subjectType': self.subjectType
        }
        response = requests.get(url, params=param, cookies=self.cookie, headers=self.headers)
        text = response.text
        soup = BeautifulSoup(text, 'html.parser')
        url = soup.find('a', id='topic_start_btn').get('href')
        paperid = re.findall('paperid=(.*?)&', url)[0]
        self.paperid = paperid
        self.log(f"Paper ID: {self.paperid}")

    def get_testid(self):
        url = 'http://mapp.nudt.edu.cn/websubject/PubRandomSubject.do'
        param = {
            'roomid': self.roomid,
            'subjectType': self.subjectType,
            'paperid': self.paperid,
            'timelen': 60,
            'screenWidth': 390,
        }
        response = requests.get(url, params=param, cookies=self.cookie, headers=self.headers)
        html = response.text
        self.testid = re.findall(r'var testid = "(.*?)";', html)[0]
        self.versionId = re.findall(r'var versionId = "(.*?)";', html)[0]
        self.subjectId = re.findall(r'var subjectId = "(.*?)";', html)[0]
        self.loginUserId = re.findall(r"'loginUserId': '(.*?)',", html)[0]
        self.log(f"Test ID: {self.testid}, Version ID: {self.versionId}, Subject ID: {self.subjectId}, Login User ID: {self.loginUserId}")
        return self.testid
        
    def analyze_question(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        button = soup.find('div', class_='side_unit_info')
        url = button.text
        ind = re.findall(r'第(.*?)题', button.text,re.S)[0]
        q_type = re.findall(r'题\xa0\n                                            (.*?)/\xa0', button.text,re.S)[0]
        q_img_url = soup.find('img', style="width: 100%").get('src')
        anserbox = soup.find('div', class_='answerUnitViewBox')
        ul = anserbox.ul
        choices = []
        for li in ul.find_all('li'):
            #print(li)
            choice = li.label.text.replace(' ', '').replace('\n', '') # 选项
            value = li.input.get('value')
            choices.append((choice, value))
        return ind, q_type, q_img_url, choices
    
    def get_review(self):
        url = 'http://mapp.nudt.edu.cn/websubject/testCardSubjectReview.do'
        param = {
            'testid': self.testid,
        }
        response = requests.get(url, params=param, cookies=self.cookie, headers=self.headers)
        if response.status_code != 200:
            raise Exception("Get review failed.")
        html = response.text
        return html

    def get_ans(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        big_div = soup.find('div', class_='container wts-paper-forms')
        raw_divs = list(big_div.children)[7:]
        divs = []
        for div in raw_divs:
            if div == '\n':
                continue
            divs.append(div)
        # '\n                                第1题\xa0 多选题\xa0\n\n\n\n\n\n                            '
        type_list = ['填空', '单选', '多选', '判断', '问答']

        qs = []
        for div in divs:
            title = div.find('div', class_='side_unit_info')
            ind = re.findall(r'第(.*?)题', title.text,re.S)[0]
            for t in type_list:
                if t in title.text:
                    q_type = t
                    break

            try:
                q_img_url = div.find('img', style="width: 100%").get('src')
            except:
                text = div.find('div', style="text-align: left;").text
                cut_key = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
                q_img_url = None

            if q_type == '填空':
                ans = re.findall(r'正确答案：(.*?)\n', div.text, re.S)[0]
                # choice = re.findall(r'id="(.*?)-INPUT">', div.contents[1], re.S)[0]
                pattern = r'id="([^"]+-INPUT)'
                match = re.search(pattern, str(div.contents[1]))

                if match:
                    choice = match.group(1)[:-6]
                    print("ID值是:", choice)
                else:
                    print("未找到ID值")
                
                choices = [(ans, choice)]
                #self.log(div.text)
                print(ind, q_type, q_img_url)
                right_ans = [choice]
            else:
                anserbox = div.find('div', class_='answerUnitViewBox')
                ul = anserbox.ul
                choices = []
                for li in ul.find_all('li'):
                    #print(li)
                    choice = li.label.text.replace(' ', '').replace('\n', '').replace('\xa0', '') # 选项

                    value = li.input.get('value')
                    choices.append((choice, value))
                    #print()
                    #print()
                a_div = div.find('div', class_='answerRightViewBox')
                labels = a_div.find_all('label')
                print(ind, q_type, q_img_url)
                print(choices)
                right_ans = []
                for label in labels:
                    right_ans.append(label.get('for').replace('-INPUT', ''))
                    #print(label.get('for').replace('-INPUT', ''))
                print(right_ans)
            self.log(f"Question {ind}: {q_type}, Choices: {choices}, Right Answers: {right_ans}")
            qs.append((ind, q_type, choices, right_ans))
        return qs
    
    def submit_ans(self, choices, right_ans, qtype):
        url = 'http://mapp.nudt.edu.cn/websubject/PubRunPoint.do'
        val = []
        for i, choice in enumerate(choices):
            
            if choice[1] in right_ans:
                isR = True
            else:
                isR = False
                
            if qtype == '填空':
                isR = choice[0]

            d = {
                'versionid':self.versionId,
                'answerid':choice[1],
                'value': isR,
            }
            #d = json.dumps(d)
            val.append(d)
        #val = json.dumps(val).replace('\\', '')
        post_data = {
            'testid': self.testid,
            'versionId': self.versionId,
            'val':val,
            'loginUserId': self.loginUserId,
            'screenWidth': 390,
            
        }

        post_data['val'] = json.dumps(post_data['val']).replace(' ', '')
        encoded_data = urlencode(post_data)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 9; COL-AL10 Build/HUAWEICOL-AL10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/85.0.3527.52 MQQBrowser/6.2 TBS/044607 Mobile Safari/537.36 MMWEBID/7140 MicroMessenger/7.0.4.1420(0x27000437) Process/tools NetType/4G Language/zh_CN',
            'Accept': '*/*',
            'Host': 'mapp.nudt.edu.cn',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded'
            }
        response = requests.post(url, data=encoded_data, headers=headers, cookies=self.cookie)
        while response.status_code != 200:
            self.log(response.text)
            response = requests.post(url, data=encoded_data, headers=headers, cookies=self.cookie)
        if response.status_code == 200:
            print(response.text)
            self.log(response.text)
            if response.text != '{"OPERATE":3,"STATE":0,"point":100}':
                raise SubAnswerError("Submit failed.")
            print('Submit successfully.')
            return 0
        else:
            print(response.text)
            raise SubAnswerError("Submit failed.")
        
    def get_result(self, id = 11):
        url = 'http://mapp.nudt.edu.cn/websubject/PubRandomSubject.do'
        param = {
            'index':id,
            'totalTime': 0,
            'testid': self.testid,
            'subjectType': self.subjectType,
            'userTestUuid': self.loginUserId,
        }
        response = requests.get(url, params=param, cookies=self.cookie, headers=self.headers)
        html = response.text
        try:
            self.versionId = re.findall(r'var versionId = "(.*?)";', html)[0]
        except:
            # print(html)
            if "本次答题时间异常，不记录成绩，请重新答题！" in html:
                print("本次答题时间异常，不记录成绩，请重新答题！")
                self.log("本次答题时间异常，不记录成绩，请重新答题！")
                raise SubTimeError("Time error")

            print(html)
        
        if id == 11:
            try:
                jf = re.findall('共获得(.*?)积分', html)[0]
                print("共获得"+str(jf)+"积分")
                self.log("共获得"+str(jf)+"积分")
                self.jf = jf
                return jf
            except:
                if "正确:10" in html:
                    print("今日得分上限")
                    raise Exception("今日得分上限")
                    return True
                return False
        else:
            print('Get VersionID')
            return True
    def close(self):
        self.log('Finish')
        self.f.close()
        return 'Finish'



if __name__ == '__main__':
    pass