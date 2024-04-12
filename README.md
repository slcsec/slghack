# slghack - Google Hacking

## 描述

slghack 是一个基于 python 第三方库 [yagooglesearch](https://pypi.org/project/yagooglesearch/) 开发的自动化 google hacking 搜索工具。

- 支持使用 google hacking 语法单一搜索

- 支持指定包含 dorks 的文件批量搜索（包含文件中的 dork 必须是一行一个）

    更多的 dorks 请参考 [Google Hacking Database](https://www.exploit-db.com/google-hacking-database)

- 支持使用代理


Google 有很强地反爬虫能力，一般的爬虫会很快被封IP。

yagooglesearch 是一个 Python 库，可以模拟真实的人类谷歌搜索行为，可以有效防止 Google 429 响应。

**注意：**爬取谷歌搜索结果可能会违反他们的服务条款，所以使用谷歌的首选方法是使用它们的 [API]([Custom Search JSON API  | Programmable Search Engine  | Google for Developers](https://developers.google.com/custom-search/v1/overview?hl=zh-cn)) 。

## 使用

脚本使用Python3开发

```bash
git clone 
cd slghack
python slghack.py -h
```


![image-20240412180117316](D:\JetBrains\PyCharm-workspaces\slghack\images\image-20240412180117316.png)

