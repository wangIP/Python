def start_download(count,url, treeview,folder):
    ydl_opts = {
        "format": "best",
        'outtmpl': folder+'\%(title)s.%(ext)s',
    }
    ydl = YoutubeDL(ydl_opts)
    res = ydl.extract_info(url, download=False)
    name = res["title"]
    # ---------------↓ 鎖定區域 A ↓---------------#
    lock.acquire()  # 進行鎖定
    treeview_data = []
    treeview_data.append(name)

    treeview.insert( parent='',index="end",iid=count ,values=(count,treeview_data[0],'下載中'))
    print("插入:", count, name)
    lock.release()  # 釋放鎖定
    # ---------------↑ 鎖定區域 A ↑---------------#
    ydl.download([url])  # 開始下載影片 (不可鎖定)
    # ---------------↓ 鎖定區域 B ↓---------------#
    lock.acquire()  # 進行鎖定
    print("更新:", count, name)
    treeview.delete(count)
    treeview.insert(parent='',index="end",iid=count ,values=(count,treeview_data[0],'下載完成'))
    lock.release()  # 釋放鎖定
    # ---------------↑ 鎖定區域 B ↑---------------#