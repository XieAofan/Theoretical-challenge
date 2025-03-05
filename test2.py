import requests

url = "http://mapp.nudt.edu.cn/websubject/PubRunPoint.do"

payload1='testid=774d8c09fded481fabdf67f1b80928a0&versionId=8a9496479490f1ab019490f6ef43005b&val=%5B%7B%22versionid%22%3A%228a9496479490f1ab019490f6ef43005b%22%2C%22answerid%22%3A%22MbsNooVmAhxIFJG8EuhxXmqJ1WwKHW1GW9geH9Io3jIvQ92YGrjGpZpZ8CrVCmHb%22%2C%22value%22%3Afalse%7D%2C%7B%22versionid%22%3A%228a9496479490f1ab019490f6ef43005b%22%2C%22answerid%22%3A%22zUDwONuHBTE8fEkhFVeJb24KNa2%2FM%2BBQCYVRPC072d1rmAB0uQqmegXWx8HEpaGK%22%2C%22value%22%3Atrue%7D%5D&loginUserId=3b37e5d6ac7d456cb94cc77b52d140d4&screenWidth=390'
payload2='testid=774d8c09fded481fabdf67f1b80928a0&versionId=8a9496479490f1ab019490f6ef43005b&val=%5B%7B%22versionId%22%3A%228a9496479490f1ab019490f6ef43005b%22%2C%22answerid%22%3A%22MbsNooVmAhxIFJG8EuhxXmqJ1WwKHW1GW9geH9Io3jIvQ92YGrjGpZpZ8CrVCmHb%22%2C%22value%22%3Afalse%7D%2C%7B%22versionId%22%3A%228a9496479490f1ab019490f6ef43005b%22%2C%22answerid%22%3A%22zUDwONuHBTE8fEkhFVeJb24KNa2%2FM%2BBQCYVRPC072d1rmAB0uQqmegXWx8HEpaGK%22%2C%22value%22%3Atrue%7D%5D&loginUserId=3b37e5d6ac7d456cb94cc77b52d140d4&screenWidth=390'
print(len(payload1), len(payload2))
if payload1 == payload2:
    print(True)
    print(len(payload1), len(payload2))
else:
    for i in range(len(payload1)):
        if payload1[i] != payload2[i]:
            print(i)
            print(payload1[i:i+10])
            print(payload2[i:i+10])
            break
headers = {
   'User-Agent': 'Mozilla/5.0 (Linux; Android 9; COL-AL10 Build/HUAWEICOL-AL10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/85.0.3527.52 MQQBrowser/6.2 TBS/044607 Mobile Safari/537.36 MMWEBID/7140 MicroMessenger/7.0.4.1420(0x27000437) Process/tools NetType/4G Language/zh_CN',
   'Cookie': 'JSESSIONID=9218E87364A8D217155D740D2C1B93A1',
   'Accept': '*/*',
   'Host': 'mapp.nudt.edu.cn',
   'Connection': 'keep-alive',
   'Content-Type': 'application/x-www-form-urlencoded'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)