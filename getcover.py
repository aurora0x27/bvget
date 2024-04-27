import requests
import os
import json
from lxml import etree

bv = input("input the bv number >> ")

url = f"https://www.bilibili.com/{bv}"

headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36", 
    "referer":  f"https://www.bilibili.com/video/{bv}"
}

print("==>正获取网页源代码...")
res = requests.get(url, headers = headers)

print("==>正解析网页源代码...")
html = etree.HTML(res.text)
src = str(html.xpath("/html/head/script[5]/text()")[0])
src = src[25:]
tmp = 0
src1 = ""
for i in src:
    if i == "{":
        tmp += 1
        src1 += "{"
    elif i == "}":
        tmp -= 1
        src1 += "}"
    else:
        src1 += i
    if tmp == 0:
        break

src_dict = json.loads(src1)
img_url = src_dict["videoData"]["pic"]

UserName = os.environ['USER']
path = f"/home/{UserName}/Desktop/"
s = input("input the absolute path to the image >> ")
if s != "":
	path = s
img = requests.get(img_url, headers = headers)
with open(path + f"{bv}.jpg", "wb+") as f:
    f.write(img.content)
    print("==>正写入" + f"{bv}.jpg")
