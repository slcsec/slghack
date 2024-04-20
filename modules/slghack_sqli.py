# coding:utf-8
# 利用 sqlmap API 接口联动 Google Hacking 批量 SQL 注入检测

import json
import queue
import requests
from threading import Thread
from time import sleep
 
class slghack_sqli:
    def __init__(self, server="http://127.0.0.1:8775", urlsfile=None, output="sqli_result.txt"):
        self.server = server
        self.urlsfile = urlsfile
        self.ouput = output
        self.task_queue = queue.Queue()
 
    def get_urls(self):
        with open(self.urlsfile, "r") as f:
            for url in f.readlines():
                self.task_queue.put(url.strip())
 
    def sent_server(self):
        threads = []
        while not self.task_queue.empty():
            url = self.task_queue.get().strip()
            print(f"Target URL: {url}")
            t = Thread(target=self.scan, args=(url,))
            threads.append(t)
            t.start()
 
        for t in threads:
            t.join()
 
    def scan(self, url):
        try:
            # 通过GET请求 http://ip:port/task/new 创建一个新的扫描任务
            r = requests.get(f"{self.server}/task/new")
            taskid = r.json()['taskid']
            # 通过POST请求 http://ip:port/scan/start 并通过json格式提交参数，开启一个扫描
            r = requests.post(
                f"{self.server}/scan/{taskid}/start",
                data=json.dumps({'url': url}), headers={'content-type': 'application/json'}
            )
            # 通过GET请求 http://ip:port/scan//status 来获取指定的taskid的扫描状态
            r = requests.get(f"{self.server}/scan/{taskid}/status")
            count = 0
            while r.json()["status"] == "running":
                sleep(6)
                r = requests.get(f"{self.server}/scan/{taskid}/status")
                print(r.json()["status"])
                count += 1
                if count == 30:
                    # 每个task最多跑6*30=180s结束
                    requests.get(f"{self.server}/scan/{taskid}/stop")
            r = requests.get(f"{self.server}/scan/{taskid}/data")
            requests.get(f"{self.server}/scan/{taskid}/delete")
            if r.json()['data']:
                print("Injection found: " + url)
                with open(self.ouput, "a") as f:
                    f.write(url + "\n")
        except requests.ConnectionError:
            print("Connection error!")
 
 
if __name__ == '__main__':
    # 把slghack跑的结果复制到sql_urls.txt
    ssqli = slghack_sqli(urlsfile='sql_urls.txt')
    ssqli.get_urls()
    ssqli.sent_server()
