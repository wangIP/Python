def start_download(count,url, treeview,folder,radio_var):
    """用於下載youtube的函數"""
    if radio_var == 4:
        #最高品質動画
        ydl_opts_video = {
            "format": "bestvideo/best",
            'outtmpl': folder+'\%(id)s.mp4',
        }
        ydl_video = YoutubeDL(ydl_opts_video)
        res = ydl_video.extract_info(url, download=False)
        id = res["id"]
        title = res["title"]
        treeview_data = []
        treeview_data.append(title)
        treeview.insert( parent='',index="end",iid=count ,values=(count,treeview_data[0],'下載中'))
        ydl_video.download([url])  # 開始下載影片 (不可鎖定)
        #最高品質音声
        ydl_opts_audio = {
            "format": "bestaudio/best",
            'outtmpl': folder+'\%(id)s.mp3',
        }
        ydl_audio = YoutubeDL(ydl_opts_audio)
        ydl_audio.download([url])  # 開始下載影片 (不可鎖定)
        # 定义输入视频和音频文件的路径
        mp4_path = folder+'/'+ id + '.mp4'
        mp3_path = folder+'/'+ id + '.mp3'
        # 加载输入视频和音频文件
        input_video = ffmpeg.input(mp4_path)
        input_audio = ffmpeg.input(mp3_path)
        # 合并视频和音频
        merged = ffmpeg.concat(input_video, input_audio, v=1, a=1).output(folder+'/'+ title + '.mp4', vcodec='libx264', preset='ultrafast')
        # 运行 FFmpeg 命令
        ffmpeg.run(merged)
        treeview.delete(count)
        treeview.insert(parent='',index="end",iid=count ,values=(count,treeview_data[0],'下載完成'))
    elif radio_var == 3:
        #最高品質音声
        ydl_opts_audio = {
            "format": "bestaudio/best",
            'outtmpl': folder+'\%(title)s.mp3',
        }
        ydl_audio = YoutubeDL(ydl_opts_audio)
        res = ydl_audio.extract_info(url, download=False)
        id = res["id"]
        title = res["title"]
        treeview_data = []
        treeview_data.append(title)
        treeview.insert( parent='',index="end",iid=count ,values=(count,treeview_data[0],'下載中'))
        ydl_audio.download([url])  # 開始下載影片 (不可鎖定)
        treeview.delete(count)
        treeview.insert(parent='',index="end",iid=count ,values=(count,treeview_data[0],'下載完成'))
    return id
