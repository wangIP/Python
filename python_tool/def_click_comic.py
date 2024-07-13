def click_comic(self):
        """用於動漫更新偵測的函數"""
        comic_name=self.entry_comic_name.get()
        radio_value=self.radio_var.get()
        self.count = self.count + 1
        if radio_value ==6:
            #動漫狂
            tree_comic=m.comic_get_cartoonmad(self.count,comic_name,self.treeview_comic)
        else:
            tree_comic=m.comic_get_6parkbbs(self.count,comic_name,self.treeview_comic)
        
        # 設定 Treeview 項目點擊事件
        def on_item_click(event):
            """點擊時開啟相關新聞頁面的函數""" 
            item = tree_comic.selection()[0]
            url = tree_comic.item(item, "values")[3]               
            webbrowser.open(url)
        tree_comic.bind("<Double-1>", on_item_click)  # 雙擊項目時觸發事件
import requests
import chardet
from bs4 import BeautifulSoup
def comic_get_cartoonmad(count,comic_name,treeview):
    """用於從動漫狂取得漫畫資訊函數"""
    update="否"
    url = "https://www.cartoonmad.com/"
    response = requests.get(url)
    encoding = chardet.detect(response.content)['encoding']
    response.encoding = encoding
    soup = BeautifulSoup(response.text, "lxml")
    #newを探す
    imgs = soup.find_all('img', src='/image/new.gif')
    name_list=[]
    #更新漫画がある
    if imgs != None:
        for img in imgs:
            parent_a = img.parent
            #print(parent_a.text)
            name_list.append(parent_a.text)#更新漫画名をlistに追加
        #確認したい漫画がlistに存在する場合updateをセットする
        if comic_name in name_list:
            #print(comic_name+"更新")
            update="是"
    #全部漫画名を取得
    titles = soup.find_all('a', class_='a1')
    comic_page = soup.find_all('a', class_='a2')

    title_list = []
    for title in titles:
        #print(title.text)
        title_list.append(title.text)#漫画名
    page_list=[]
    for comic_pages in comic_page:
        #print(comic_pages.text)
        #print(comic_pages.attrs['href'])
        page_list.append([comic_pages.text,url+comic_pages.attrs['href']])#漫画何話
    dictionary = dict(zip(title_list, page_list)) 
    #確認したい漫画がlistに存在する場合treeviewに挿入
    if comic_name in dictionary:
        treeview.insert( parent='',index="end",iid=count 
                        ,values=(comic_name,update,dictionary[comic_name][0],dictionary[comic_name][1]))
    
    return treeview
import zhconv
def comic_get_6parkbbs(count,comic_name,treeview):
    """用於從留園網取得漫畫資訊函數"""
    update="?"
    url = "https://club.6parkbbs.com/enter6/"
    response = requests.get(url)
    #encoding = chardet.detect(response.content)['encoding']
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, "lxml")
    #newを探す
    #imgs = soup.find_all('img', src='/image/new.gif')
    divs = soup.find(id='d_gold_list')
    name_list=[]
    name_url=[]
    tables = divs.find_all('table')
    for table in tables:
        tds = table.find_all('td')
        for td in tds:
            a_tags = td.find_all('a')
            for a in a_tags:
                #print(a)
                name_list.append(a.text)
                name_url.append(a.attrs['href'])
    for id,name in enumerate(name_list):
        comic_name_conv=zhconv.convert(comic_name, 'zh-cn')
        if comic_name_conv in name:
            treeview.insert( parent='',index="end",iid=count 
                        ,values=(comic_name,update,name_list[id],url+name_url[id]))
        
    return treeview