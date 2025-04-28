import requests, time
from lxml import etree
from fake_useragent import UserAgent
from pypinyin import lazy_pinyin

url = "https://alhs.xyz/index.php/archives/2020/09/2536/"


ua = UserAgent()
proxies = {
    "http": "http://127.0.0.1:7890",
    "https": "http://127.0.0.1:7890"
}

# 随机生成一个 User-Agent
headers = {
    "User-Agent": ua.random
}


response = requests.get(url, headers=headers, proxies=proxies)


# 解析 HTML
tree = etree.HTML(response.text)
title_element = tree.xpath('/html/head/title')
page_title = title_element[0].text  # 提取 <title> 标签的文本内容
# print(page_title)
pl = page_title.split('-')
url_list = [[url, pl[0][:-1]]]

li_elements = tree.xpath('/html/body/div[4]/div[5]/main/article/div[1]/section/ul/li')
n = len(li_elements)
for li in li_elements[1:]:
    # 获取每个 li 元素中的文本内容
    a = li.xpath('.//span/a')
    text = a[0].text
    url = a[0].get('href')
    url_list.append([url, text])


# print(url_list)
url_list = sorted(url_list, key=lambda x: (
    # 提取年、月、末尾数字（根据URL结构调整索引位置）
    int(x[0].split('/')[-4]),  # 年
    int(x[0].split('/')[-3]),  # 月
    int(x[0].split('/')[-2])   # 末尾数字
))
# print(url_list)

# 在排序后添加去重逻辑（保留顺序）
seen_urls = set()
url_list = [x for x in url_list if not (x[0] in seen_urls or seen_urls.add(x[0]))]

def get_text(tree):
    text = ''
    p_elements = tree.xpath('/html/body/div[4]/div[5]/main/article/div[1]/p')
    for idx, p in enumerate(p_elements, start=1):
        text += p.text.strip() if p.text else "无文本内容"  # 去除多余空格或处理空文本
        text += '\n' 
    return text

i = 1
charpter_list = []
for url in url_list:
    print(f"{i}/{n}\t", url[1],'\t',url[0])
    i += 1
    if url[0] == url_list[0][0]:
        pass
    else:
        time.sleep(1)
        response = requests.get(url[0], headers=headers, proxies=proxies)
        tree = etree.HTML(response.text)
    text = get_text(tree)
    charpter_list.append([url[1], text])


f = open(f'out.txt', 'w', encoding='utf-8')
for idx, t in enumerate(charpter_list):
    f.write(f'第{idx+1}章 {t[0]}\n\n{t[1]}\n\n\n')
f.close()