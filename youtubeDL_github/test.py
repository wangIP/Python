# from pytube import YouTube

# url= 'https://www.youtube.com/watch?v=Je6r_DqkPqU'

# yt = YouTube(url)

# video_stream = yt.streams.all()

# download_path = 'D:\work\programming\Python\youtubeDL'

# video_stream.download(output_path=download_path)

# print('成功')
import yt_dlp
url = "https://www.youtube.com/watch?v=JrgR2V5lLRU"
ydl_opts={
    'format':'best'
}
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])
print("download",url)