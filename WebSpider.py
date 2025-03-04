import requests
import re
from bs4 import BeautifulSoup


class Web:
    def __init__(self):
        self.cookie = None
        self.roomid = None
        self.paperid = None
        self.headers = {
            "User-Agent": "Mozilla/5.0+(Linux;+Android+10;+ELE-AL00+Build/HUAWEIELE-AL00;+wv)+AppleWebKit/537.36+(KHTML,+like+Gecko)+Version/4.0+Chrome/78.0.3904.62+XWEB/2691+MMWEBSDK/200901+Mobile+Safari/537.36+MMWEBID/215+MicroMessenger/7.0.19.1760(0x2700133F)+Process/toolsmp+WeChat/arm64+NetType/WIFI+Language/zh_CN+ABI/arm64"
        }
    
    def login(self, username, password):
        headers = {
            "User-Agent": "Mozilla/5.0+(Linux;+Android+10;+ELE-AL00+Build/HUAWEIELE-AL00;+wv)+AppleWebKit/537.36+(KHTML,+like+Gecko)+Version/4.0+Chrome/78.0.3904.62+XWEB/2691+MMWEBSDK/200901+Mobile+Safari/537.36+MMWEBID/215+MicroMessenger/7.0.19.1760(0x2700133F)+Process/toolsmp+WeChat/arm64+NetType/WIFI+Language/zh_CN+ABI/arm64"
        }
        url = 'http://mapp.nudt.edu.cn/login/webout.do'
        be = requests.get(url, headers=headers)
        cookie = be.cookies
        cookie = cookie.items()
        cookie = dict(cookie)
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
        url = 'http://mapp.nudt.edu.cn/login/login.do'
        response = requests.post(url, data=post_data, cookies=cookie, headers=headers)
        print(response.status_code)
        if response.status_code == 200:
            self.cookie = cookie
        else:
            raise Exception("Login failed.")
        
    def get_roomid(self):
        url = 'http://mapp.nudt.edu.cn/home/answerRoom.do'
        response = requests.get(url, cookies=self.cookie, headers=self.headers)
        text = response.text
        soup = BeautifulSoup(text, 'html.parser')
        button = soup.find('button', class_='loginbtn')
        text = button.get('onclick')
        #print(text)
        match = re.search(r"submitRoomPage\('([^']+)','([^']+)'\)", text)
        type = match.groups()[0]
        roomid = match.groups()[1]
        self.roomid = roomid
        self.subjectType = type

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


if __name__ == '__main__':
    web = Web()
    web.login('pctest', '954321')