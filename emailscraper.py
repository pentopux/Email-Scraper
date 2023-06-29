import os
import re
import random
import time
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor
import requests
from bs4 import BeautifulSoup as bs
from colorama import Fore

requests.packages.urllib3.disable_warnings()

max_num = 10000  # Max Urls To scrape through
num_url = 0
main_url = input("[ -INPUT- ] Website Url: ")

domain = urlparse(main_url).netloc

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 11.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "close",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
    "TE": "trailers",
}

cyan = Fore.CYAN
white = Fore.WHITE
red = Fore.RED
green = Fore.GREEN

emails__ = set()
urls = set()

def save_results():
    with open("emails__.txt", "w") as file:
        for email in emails__:
            file.write(email + "\n")

def find_emails(content):
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'
    emails = re.findall(pattern, content)
    for email in emails:
        if email not in emails__:
            print(f"{red}[ {cyan}INFO {red}] {green}Found New Email: {white}{email}")
            emails__.add(email)

def scrape(url):
    time.sleep(random.randint(1,10))
    short_url = url[:80] + '...' if len(url) > 80 else url
    global num_url
    if num_url >= max_num:
        save_results()
        os._exit(0)
    num_url += 1
    urls_list = set()
    print(f"{cyan}[ {red}SPIDER {num_url}{cyan} ]{white} {short_url}")
    try:
        with requests.Session() as session:
            content = session.get(url, headers=headers, verify=False, timeout=10).text
    except requests.RequestException:
        content = "error"
    find_emails(content)
    soup = bs(content, 'html.parser')
    anchor_tags = soup.find_all("a")
    for anchor in anchor_tags:
        href = anchor.get('href')
        if href:
            if href.startswith("/"):
                url = urljoin(url, href)
            elif href.startswith("http://") or href.startswith("https://"):
                url = href
            if url not in urls:
                if domain in urlparse(url).netloc: # remove this to scrape outside of the website
                    urls.add(url)
                    urls_list.add(url)
    with ThreadPoolExecutor(max_workers=random.randint(1,3)) as executor:
        executor.map(scrape, urls_list)

try:
    scrape(main_url)
except KeyboardInterrupt:
    save_results()
    print(f"\n{cyan}[ {red}INTERRUPTED {cyan}]{white} Saved Results To emails__.txt")
    os._exit(0)


print(f"{cyan}[ {green}FINISHED {cyan}]{white} Saved Results To emails__.txt")
