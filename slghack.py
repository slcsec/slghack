import argparse
import random
import sys
import datetime
import time

import yagooglesearch

red = '\033[1;31m'
green = '\033[01;32m'
yellow = '\033[01;33m'
blue = '\033[01;34m'
end = '\033[0m'

version = 'v.0.1'
message = f"{version}@smileleooo"

slghack_banner = f"""
slghack is a tool that uses Google search technology to collect urls in bulk.{red}
       __     __            __  
  ___ / /__ _/ /  ___ _____/ /__{green}
 (_-</ / _ `/ _ \/ _ `/ __/  '_/{yellow}
/___/_/\_, /_//_/\_,_/\__/_/\_\ {blue}
      /___/                     {end}{message}
      
Type 'python slghack.py -h' for more information.
"""


def get_parameters():
    parser = argparse.ArgumentParser(
        description=f"slghack - Google Hacking {version}",
        formatter_class=CustomHelpFormatter,
    )
    parser.add_argument(
        "-d",
        "--domain",
        type=str,
        default="",
        required=False,
        help="Domain to scope the Google dork searches (指定搜索的域名)"
    )
    parser.add_argument(
        '-q',
        '--query-dork',
        type=str,
        default="",
        required=False,
        help="Follow the Google Hacking search syntax (按照 Google Hacking 语法搜索)"
    )
    parser.add_argument(
        "-g",
        "--google-dorks-file",
        default=None,
        required=False,
        help="File containing Google dorks (载入dorks文件搜索)"
    )
    parser.add_argument(
        "-m",
        "--max-result-to-return",
        type=int,
        default=100,
        required=False,
        help="Maximum results to return per dork, Default: 100 (搜索每个dork返回URL的最大数量)"
    )
    parser.add_argument(
        "-p",
        "--proxy",
        type=str,
        default="",
        required=False,
        help="Using a proxy, Example: 'http://localhost:7890' (使用代理访问)"
    )
    parser.add_argument(
        "-o",
        "--output-file",
        nargs="?",
        default=None,
        help="Export results to a file, Default: results_<time>.txt (保存URL到文件)"
    )
    parser.add_argument(
        "-v",
        "--verbosity",
        type=int,
        default=4,
        help="Verbosity level (0=NOTSET, 1=CRITICAL, 2=ERROR, 3=WARNING, 4=INFO, 5=DEBUG) Default: 4"
    )

    return parser.parse_args()


class CustomHelpFormatter(argparse.HelpFormatter):
    def add_usage(self, usage, actions, groups, prefix=None):
        if prefix is None:
            prefix = 'usage: '
        return super().add_usage(usage, actions, groups, prefix)

    def format_help(self):
        return f"{slghack_banner}\n" + super().format_help()


class SLGHack:
    def __init__(self, domain="", query_dork="", google_dorks_file=None, max_result_to_return=100,
                 proxy="", output_file=None, verbosity=4):
        self.domain = domain.strip()
        self.query_dork = query_dork.strip()
        self.google_dorks_file = google_dorks_file
        self.max_result_to_return = max_result_to_return
        self.proxy = proxy.strip()
        self.output_file = output_file
        self.verbosity = verbosity

        self.minimum_delay_seconds = 40
        self.maximum_delay_seconds = 60
        self.random_delays_list = self.random_delays()
        self.query_dorks = []
        self.results_list = []

        if self.output_file is None:
            self.output_file = f'results-{datetime.datetime.now().strftime("%H%M%S")}.txt'

    # 产生一个随机数列表，用于两次搜索之间的延时时间
    def random_delays(self):
        delays = [
            random.uniform(self.minimum_delay_seconds, self.maximum_delay_seconds)
            for i in range(10)
        ]
        rounded_delays = [round(delay, 1) for delay in delays]
        return sorted(rounded_delays)

    def search(self):
        query_domain = ''
        if self.domain:
            query_domain = f"site:{self.domain}".strip()
            self.query_dorks.append(query_domain)

        if self.query_dork and self.google_dorks_file is None:
            self.query_dorks = []
            query = f"{query_domain} {self.query_dork}".strip()
            self.query_dorks.append(query)

        if self.google_dorks_file:
            self.query_dorks = []
            if self.query_dork:
                # 在指定文件的同时，又使用 -q 输入单个dork，同样将该dork添加到查询列表query_dorks
                self.query_dorks.append(f"{query_domain} {self.query_dork}".strip())
            with open(self.google_dorks_file, "r", encoding="utf-8") as f:
                for line in f.read().splitlines():
                    self.query_dorks.append(f"{query_domain} {line}".strip())

        # print(self.query_dorks)

        for query in self.query_dorks:
            try:
                query = query.strip()

                # 给每一个query实例化一个yagooglesearch.SearchClient对象
                client = yagooglesearch.SearchClient(
                    query,
                    tbs="li:1",  # 逐字搜索或时间限制
                    num=100,  # 每一页拉回结果的最大数量 (Google上限为100)
                    max_search_result_urls_to_return=self.max_result_to_return,
                    proxy=self.proxy,
                    verbosity=self.verbosity
                )

                client.assign_random_user_agent()
                # 搜索
                self.results_list = client.search()

                if self.results_list:
                    if self.output_file:
                        with open(self.output_file, "a") as f:
                            for url in self.results_list:
                                f.write(f"{url}\n")
                else:
                    print(f"{red}No Google dork results found.{end}")

            except KeyboardInterrupt:
                sys.exit(0)

            # 随机延时搜索，防止被Google阻塞IP
            if query != self.query_dorks[-1]:
                pause_time = random.choice(self.random_delays_list)
                print(f"The dork query {blue}'{query}'{end} has been completed, "
                      f"the next query is executed after {yellow}{pause_time}{end} seconds...")
                time.sleep(pause_time)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print(slghack_banner)
    else:
        slghack = SLGHack(**vars(get_parameters()))
        slghack.search()
