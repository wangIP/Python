from bs4 import BeautifulSoup
import requests
import threading
from pytube import YouTube
import tkinter as tk
from datetime import datetime
from yt_dlp import YoutubeDL


def get_urls(url):
    index=url.find('channel/')
    r= url[index+len('channel/'):]
    YOUTUBE_API_KEY = "api-key"
    youtube_channel_id = r
    

    youtube_spider = YoutubeSpider(YOUTUBE_API_KEY)
    uploads_id = youtube_spider.get_channel_uploads_id(youtube_channel_id)
    #print(uploads_id)

    video_ids = youtube_spider.get_playlist(uploads_id, max_results=20)
    
    #print(video_ids)
    list = []
    for video_id in video_ids:
        print("----------------------")
        video_info = youtube_spider.get_video(video_id)
        # print(video_info)
        list.append(video_info)
    return list
lock = threading.Lock()
def start_dload(url, listbox):
    ydl_opts={
    'format':'best',
    'output':'file_path%(title)s.%(ext)s'
    }
    ydl = YoutubeDL(ydl_opts)
    # ydl.download([url])
    res=ydl.extract_info(url,download=False)
    
    # name = ydl.title
    name = res['title']
    #---------------↓ 鎖定區域 A ↓---------------#
    lock.acquire()              # 進行鎖定
    no = listbox.size()     # 以目前列表框筆數為下載編號
    listbox.insert(tk.END, f'{no:02d}:{name}.....下載中')
    print('插入:', no, name)
    lock.release()              # 釋放鎖定
    #---------------↑ 鎖定區域 A ↑---------------#
    ydl.download([url])   # 開始下載影片 (不可鎖定)
    #---------------↓ 鎖定區域 B ↓---------------#
    lock.acquire()              # 進行鎖定
    print('更新:', no, name)
    listbox.delete(no)
    listbox.insert(no, f'{no:02d}:●{name}.....下載完成')
    lock.release()              # 釋放鎖定
    #---------------↑ 鎖定區域 B ↑---------------#
class YoutubeSpider():
    def __init__(self, api_key):
        self.base_url = "https://www.googleapis.com/youtube/v3/"
        self.api_key = api_key

    def get_html_to_json(self, path):
        """組合 URL 後 GET 網頁並轉換成 JSON"""
        api_url = f"{self.base_url}{path}&key={self.api_key}"
        r = requests.get(api_url)
        if r.status_code == requests.codes.ok:
            data = r.json()
        else:
            data = None
        return data

    def get_channel_uploads_id(self, channel_id, part='contentDetails'):
        """取得頻道上傳影片清單的ID"""
        # UC7ia-A8gma8qcdC6GDcjwsQ
        path = f'channels?part={part}&id={channel_id}'
        data = self.get_html_to_json(path)
        try:
            uploads_id = data['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        except KeyError:
            uploads_id = None
        return uploads_id

    def get_playlist(self, playlist_id, part='contentDetails', max_results=10):
        """取得影片清單ID中的影片"""
        # UU7ia-A8gma8qcdC6GDcjwsQ
        path = f'playlistItems?part={part}&playlistId={playlist_id}&maxResults={max_results}'
        data = self.get_html_to_json(path)
        if not data:
            return []

        video_ids = []
        for data_item in data['items']:
            video_ids.append(data_item['contentDetails']['videoId'])
        return video_ids

    def get_video(self, video_id, part='snippet,statistics'):
        """取得影片資訊"""
        # jyordOSr4cI
        # part = 'contentDetails,id,liveStreamingDetails,localizations,player,recordingDetails,snippet,statistics,status,topicDetails'
        path = f'videos?part={part}&id={video_id}'
        data = self.get_html_to_json(path)
        if not data:
            return {}
        # 以下整理並提取需要的資料
        data_item = data['items'][0]

        try:
            # 2019-09-29T04:17:05Z
            time_ = datetime.strptime(data_item['snippet']['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')
        except ValueError:
            # 日期格式錯誤
            time_ = None

        url_ = "https://www.youtube.com/watch?v="+data_item['id']

        info = {
            'id': data_item['id'],
            'channelTitle': data_item['snippet']['channelTitle'],
            'publishedAt': time_,
            'video_url': url_,
            'title': data_item['snippet']['title'],
            'description': data_item['snippet']['description'],
            'likeCount': data_item['statistics']['likeCount'],
            # 'dislikeCount': data_item['statistics']['dislikeCount'],
            'commentCount': data_item['statistics']['commentCount'],
            'viewCount': data_item['statistics']['viewCount']
        }
        return url_