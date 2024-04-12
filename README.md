# slghack - Google Hacking

## 描述

slghack 是一个基于 Python 第三方库 [yagooglesearch](https://pypi.org/project/yagooglesearch/) 开发的自动化 google hacking 搜索工具。

- 支持使用 google hacking 语法单一搜索

- 支持指定包含 dorks 的文件批量搜索（文件中的 dork 必须是一行一个）

    更多的 dorks 请参考 [Google Hacking Database](https://www.exploit-db.com/google-hacking-database)

- 支持使用代理


Google 有很强地反爬虫能力，一般的爬虫会很快被封IP。

yagooglesearch 是一个 Python 库，可以模拟真实的 Google 搜索行为，可以有效防止 Google 429 响应。

**注意：** 爬取 Google 搜索结果可能会违反他们的服务条款，所以使用 Google 的首选方法是使用它们的官方 [API]((https://developers.google.com/custom-search/v1/overview?hl=zh-cn)) 。

## 使用

该脚本使用Python3开发，且依赖第三方库。

![image-20240412180117316](https://github.com/zhx-hex/slghack/blob/master/images/image-20240412180117316.png)

**安装**

```bash
git clone https://github.com/zhx-hex/slghack.git
cd slghack
python slghack.py -h
```

**安装依赖**

```bash
pip install yagooglesearch
```

**参数**

```bash
usage: slghack.py [-h] [-d DOMAIN] [-q QUERY_DORK] [-g GOOGLE_DORKS_FILE] [-m MAX_RESULT_TO_RETURN]
    [-p PROXY] [-o [OUTPUT_FILE]] [-v VERBOSITY]

slghack - Google Hacking v.0.1

options:
  -h, --help            show this help message and exit
  -d DOMAIN, --domain DOMAIN
                        Domain to scope the Google dork searches (指定搜索的域名)
  -q QUERY_DORK, --query-dork QUERY_DORK
                        Follow the Google Hacking search syntax (按照 Google Hacking 语法搜索)
  -g GOOGLE_DORKS_FILE, --google-dorks-file GOOGLE_DORKS_FILE
                        File containing Google dorks (载入dorks文件搜索)
  -m MAX_RESULT_TO_RETURN, --max-result-to-return MAX_RESULT_TO_RETURN
                        Maximum results to return per dork, Default: 100 (搜索每个dork返回URL的最大数量)
  -p PROXY, --proxy PROXY
                        Using a proxy, Example: 'http://localhost:7890' (使用代理访问)
  -o [OUTPUT_FILE], --output-file [OUTPUT_FILE]
                        Export results to a file, Default: results_<time>.txt (保存URL到文件)
  -v VERBOSITY, --verbosity VERBOSITY
                        Verbosity level (0=NOTSET, 1=CRITICAL, 2=ERROR, 3=WARNING, 4=INFO, 5=DEBUG) Default: 4
```

**Examples**

指定搜索的域名为qq.com，url中包含/admin关键字，返回50个搜索结果 ，保存到qq.com.txt文件

```bash
python slghack.py -d qq.com -q inurl:/admin -m 50 -o qq.com.txt
```

指定搜索的域名为baidu.com，使用dork文件批量搜索，使用代理`http://localhost:7890`，保存到默认文件 

```bash
python slghack.py -d baidu.com -g .\dorks\sqli.txt -p http://localhost:7890 -o
```

------

**声明**

仅供技术交流，若用于非法用途，概不负责！

