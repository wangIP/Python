from bs4 import BeautifulSoup
import requests
from pytube import YouTube

def get_urls(url):
    urls = []
    if '&list' not in url : return urls
    response = requests.get(url)
    if response.status_code != 200:
        print('error')
        return
    bs = BeautifulSoup(response.text,'lxml')
    a_list = bs.find_all('a')
    base = 'https://www.youtube.com/'
    for a in a_list:
        href = a.get('href')
        url = base + href
        if ('&index=' in url) and (url not in urls):
            urls.append(url)
    return urls
