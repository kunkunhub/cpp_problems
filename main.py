from os import path
import requests
import os
import re
import threading
import time

root = os.path.dirname(__file__)
index = []
plist = []
os.chdir(root)

# 函数是个好东西

def write(file: str, text: str):
    """
    写一个文件
    """
    f = open(os.path.join(root, file), "w", encoding="utf-8")
    f.write(text)
    f.close()

def read(file: str):
    """
    读一个文件
    """
    f = open(os.path.join(root, file), "r", encoding="utf-8")
    text = f.read()
    f.close()
    return text

def getpage(url:str):
    """
    爬取一页
    """
    r = requests.get(url)
    r.encoding='utf-8'
    return r.text

def getindex():
    """
    爬取题目列表
    """
    try:
        os.mkdir("index")
        for i in range(1, 26):
            x = getpage(f"http://go.helloworldroom.com:50080/problems?page={i}")
            index.append(x)
            #x = x.replace("/problem/", os.path.join(root, "problems\\p"))
            write(f"index\i{i}.html", x)
    except FileExistsError:
        for i in os.listdir("index"):
            index.append(read(f"index\\{i}")) 


def getplist():
    """
    解析题目列表
    """
    numre = re.compile(r"\d+")
    urlre = re.compile(r"/problem/\d+")
    for i in index:
        for j in urlre.findall(i):
            plist.extend(numre.findall(j))

def getall():
    """
    爬下所有题目
    """
    os.mkdir("problems")
    def getone(n):
        text = getpage(f"http://go.helloworldroom.com:50080/problem/{n}")
        write(f"problems\p{n}.html", text)
    pool = []
    i = 0
    try:
        while True:
            if len(threading.enumerate()) <= 30:
                threading.Thread(target=getone, args=(plist[i] ,)).start()
                i += 1
            print(i, end="\r")
    except IndexError:
        pass

def main():
    """
    面函数
    """
    # 如此简洁
    print("爬取页面列表...")
    getindex()
    print("完成")
    print("解析中...")
    getplist()
    print(f"共解析到{len(plist)}个题目，开始爬取！")
    getall()
    print("完成！")
    time.sleep(1)

# 面函数
main()