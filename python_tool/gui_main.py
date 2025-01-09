"""
Example script for testing the Azure ttk theme
Author: rdbende
License: MIT license
Source: https://github.com/rdbende/ttk-widget-factory
"""


import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinterdnd2 import DND_FILES, TkinterDnD
#import threading
import method as m
import webbrowser
import os

##

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import mplfinance as mf
import matplotlib.pyplot as plt
from datetime import date, timedelta,datetime


class App(ttk.Frame):
    count_youtube_view = 0
    count_kabu_view = 0
    def __init__(self, master):
        self.root = master
        ttk.Frame.__init__(self)
        # Make the app responsive
        for index in [0, 1, 2]:
            self.columnconfigure(index=index, weight=1)
            self.rowconfigure(index=index, weight=1)
        
        self.radio_var = tk.IntVar(value=1)
        self.period_var = tk.StringVar(value=360)
        self.ma_var = tk.BooleanVar(value=False)
        self.macd_var = tk.BooleanVar(value=False)
        self.kdj_var = tk.BooleanVar(value=False)
        self.volume_var = tk.BooleanVar(value=False)
        
        # Create widgets :)
        self.setup_widgets()
        # 設置窗口關閉事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        """用於正確退出 tkinter 事件循環的函數"""
        self.root.quit()
        self.root.destroy()

    def click_youtube(self):
        """用於下載youtube影片的函數"""
        url = self.entry_youtube_url.get()
        folder=self.entry_youtube_folder.get()
        radio_value=self.radio_var.get()
        self.count_youtube_view = self.count_youtube_view + 1
        #urls = m.get_urls(url)  
        #threading.Thread(target=m.start_download, args=(self.count_youtube_view,url, self.treeview_youtube,folder)).start()
        id=m.start_download(self.count_youtube_view,url, self.treeview_youtube,folder,radio_value)
        if radio_value == 4:
            os.remove(folder+'/'+id+'.mp4')
            os.remove(folder+'/'+id+'.mp3')
            
    def folderOpen(self):
        """用於打開文件夾的函數"""
        dir = 'D:'
        fld = filedialog.askdirectory(initialdir = dir) 
        self.entry_youtube_folder.insert(0,fld)

    def changePage( self,page):
        """用於切換畫面的函數"""
        page.tkraise()
        radio_value=self.radio_var.get()
        if radio_value ==1:
            self.treeview_kabu.pack_forget()
            self.treeview_youtube.pack()
        elif radio_value == 2:         
            self.treeview_youtube.pack_forget()
            self.treeview_kabu.pack()
        elif radio_value == 3:         
            self.treeview_youtube.pack_forget()
            self.treeview_kabu.pack_forget()

    def click_kabu_year(frame,kabu,day):
            day = 365
            data_m  = m.stock_drop(kabu[0],day)
            
            fig, ax = mf.plot(data_m,title=kabu[1],style='yahoo', type='candle', figratio=(23,15),volume=True, returnfig=True)
            
            # 將圖像嵌入到 widgets_frame_yt 中
            canvas = FigureCanvasTkAgg(fig, master=frame)
            canvas.draw()
            canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

            # 添加導航工具條並放置在中央
            toolbar_frame = ttk.Frame(frame)
            toolbar_frame.grid(row=1, column=0, sticky="nsew", pady=(10, 0))
            toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
            toolbar.update()

    def click_kabu(self):
        """用於股票偵測的函數"""
        kabu_id=self.entry_kabu.get()
        kabu_id=kabu_id.strip()
        self.count_kabu_view = self.count_kabu_view + 1
        m.get_pric_etf(self.count_kabu_view,kabu_id,self.treeview_kabu)      
        def on_item_click(event):
            """點擊時彈出新視窗的函數""" 
            selected_item = self.treeview_kabu.selection()[0] 
            item_values = self.treeview_kabu.item(selected_item, "values") 
            print(f"Selected item: {item_values}") 
            recommendation = m.get_stock_buyOrSell(kabu_id)
            self.show_detail_window(item_values,recommendation)              
        self.treeview_kabu.bind("<Double-1>", on_item_click)  # 雙擊項目時觸發事件

    def click_ROI(self):
        """用於計算美日報酬率的函數"""
        item = self.treeview_kabu.selection()[0]
        m.math_ROI(self.treeview_kabu.item(item, "values")[0])

    def create_pie_chart(self, frame,buy_sell):
        """用於畫圓餅圖的函數"""
        labels = 'Buy', 'Sell'
        buy_parsennto = int(buy_sell[0])
        sell_parsennto = int(buy_sell[1])
        #center_parsennto = 100-buy_parsennto-sell_parsennto
        # sizes = [buy_parsennto, sell_parsennto,center_parsennto ]
        sizes = [buy_parsennto, sell_parsennto ]
        colors = ['gold', 'yellowgreen']
        explode = (0.1, 0)  # explode the 1st slice

        fig, ax = plt.subplots(figsize=(2, 2))
        ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=20)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        canvas = FigureCanvasTkAgg(fig, master=frame)  # A tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().pack(expand=True, fill='both')

    def toggle_indicator(self, indicator, kabu, frame):
    # Ensure mutual exclusivity of indicators
        if indicator == 'ma' and self.macd_var.get() and self.kdj_var.get():
            self.ma_var.set(False)
            return
        elif indicator == 'macd' and self.kdj_var.get() and self.ma_var.get():
            self.macd_var.set(False)
            return
        elif indicator == 'kdj' and self.macd_var.get() and self.ma_var.get():
            self.kdj_var.set(False)
            return
    
        # Toggle the indicator checkbutton and update chart
        indicator_var = getattr(self, f"{indicator}_var")
        flag = getattr(self, f"flg_{indicator.upper()}")
        
        if flag == indicator.upper():
            indicator_var.set(False)
        
        self.update_chart(kabu, frame)

    # Usage
    def toggle_ma(self, kabu, frame):
        self.toggle_indicator('ma', kabu, frame)

    def toggle_macd(self, kabu, frame):
        self.toggle_indicator('macd', kabu, frame)

    def toggle_kdj(self, kabu, frame):
        self.toggle_indicator('kdj', kabu, frame)

    def update_chart(self,kabu,frame):
        day=int(self.period_var.get())
        include_ma = self.ma_var.get() 
        include_macd = self.macd_var.get()
        include_kdj = self.kdj_var.get() 
        data_m,end_date  = m.stock_drop(kabu[0],day)
        addplot = []
        if include_ma: 
            data_m['5ma'] = data_m['Adj Close'].rolling(window=5).mean() 
            data_m['20ma'] = data_m['Adj Close'].rolling(window=20).mean() 
            data_m['60ma'] = data_m['Adj Close'].rolling(window=60).mean() 
            data_m = data_m[data_m.index >= (end_date - timedelta(days=day)).strftime('%Y-%m-%d')] 
            addplot_5ma = mf.make_addplot(data_m['5ma'], color='blue', label='5MA') 
            addplot_20ma = mf.make_addplot(data_m['20ma'], color='orange', label='20MA') 
            addplot_60ma = mf.make_addplot(data_m['60ma'], color='green', label='60MA') 
            addplot.extend([addplot_5ma, addplot_20ma, addplot_60ma]) 
            self.flg_MA = 'MA'
        else:
            self.flg_MA = ''

        if include_macd: 
            data_m['12ema'] = data_m['Adj Close'].ewm(span=12, adjust=False).mean() 
            data_m['26ema'] = data_m['Adj Close'].ewm(span=26, adjust=False).mean() 
            data_m['MACD'] = data_m['12ema'] - data_m['26ema'] 
            data_m['Signal'] = data_m['MACD'].ewm(span=9, adjust=False).mean() 
            addplot_macd = [ 
                mf.make_addplot(data_m['MACD'], panel=2, color='blue', secondary_y=False), 
                mf.make_addplot(data_m['Signal'], panel=2, color='orange', secondary_y=False), 
                mf.make_addplot(data_m['MACD'] - data_m['Signal'], type='bar', panel=2, color='gray', secondary_y=True) 
            ]
            addplot.extend(addplot_macd)
            self.flg_MACD = 'MACD'
        else:
            self.flg_MACD = ''

        if include_kdj: 
            low_list = data_m['Low'].rolling(window=9).min() 
            low_list.fillna(value=data_m['Low'].expanding().min(), inplace=True) 
            high_list = data_m['High'].rolling(window=9).max() 
            high_list.fillna(value=data_m['High'].expanding().max(), inplace=True) 
            rsv = (data_m['Adj Close'] - low_list) / (high_list - low_list) * 100 
            data_m['K'] = rsv.ewm(com=2).mean() 
            data_m['D'] = data_m['K'].ewm(com=2).mean() 
            data_m['J'] = 3 * data_m['K'] - 2 * data_m['D'] 
            if include_macd:
                addplot_k = mf.make_addplot(data_m['K'], panel=3, color='blue', secondary_y=False, label='K') 
                addplot_d = mf.make_addplot(data_m['D'], panel=3, color='orange', secondary_y=False, label='D') 
                addplot_j = mf.make_addplot(data_m['J'], panel=3, color='green', secondary_y=False, label='J')
            else:
                addplot_k = mf.make_addplot(data_m['K'], panel=2, color='blue', secondary_y=False, label='K') 
                addplot_d = mf.make_addplot(data_m['D'], panel=2, color='orange', secondary_y=False, label='D') 
                addplot_j = mf.make_addplot(data_m['J'], panel=2, color='green', secondary_y=False, label='J') 
            addplot.extend([addplot_k, addplot_d, addplot_j])
            self.flg_KDJ = 'KDJ'
        else:
            self.flg_KDJ = ''


        if include_macd and include_kdj:
            #  MACD, KDJ
            panel_ratios = (3, 1, 1, 1)
        elif include_macd or include_kdj:
            #  只有MACD或KDJ
            panel_ratios = (3, 1, 1)
        else:
            # 沒有MACD和KDJ
            panel_ratios = (3, 1)

            
        fig, ax = mf.plot(data_m, title=kabu[1], style='yahoo', type='candle', addplot=addplot, figratio=(23, 15), panel_ratios=panel_ratios, volume=True, returnfig=True)
        # 將圖像嵌入到 widgets_frame_yt 中
        self.canvas = FigureCanvasTkAgg(fig, master=frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

        # 添加導航工具條並放置在中央
        self.toolbar_frame = ttk.Frame(frame)
        self.toolbar_frame.grid(row=1, column=0, sticky="nsew", pady=(10, 0))
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.toolbar_frame)
        self.toolbar.update()

    def show_detail_window(self,kabu,buy_sell):
        """用於顯示新視窗的函數"""
        
        detail_window = tk.Toplevel(self) 
        detail_window.title("股票詳細")

        # Calculate position to center the detail_window on the screen 
        #region
        screen_width = self.winfo_screenwidth() 
        screen_height = self.winfo_screenheight() 
        window_width = screen_width // 2 +600 
        window_height = screen_height // 2 +100 
        x = (screen_width // 2) - (window_width // 2) 
        y = (screen_height // 2) - (window_height // 2) 
        detail_window.geometry(f'{window_width}x{window_height}+{x}+{y}')

        left_frame = ttk.Frame(detail_window) 
        left_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")
        
        self.left_frame_top = ttk.LabelFrame(left_frame, text="範囲", padding=(20, 5))
        self.left_frame_top.grid(row=0, column=0, padx=(20, 5), pady=(20, 5), sticky="nsew")
        self.radio_var1 = tk.IntVar(value=3)
        self.year = ttk.Radiobutton(
            self.left_frame_top, text="年", variable=self.period_var, value=365,command=lambda:self.update_chart(kabu,center_frame)
        )
        self.year.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")
        self.year_half = ttk.Radiobutton(
             self.left_frame_top, text="半年", variable=self.period_var,value=180,command=lambda:self.update_chart(kabu,center_frame)
         )
        self.year_half.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")
        #endregion
        #region#####創建 
        self.left_frame_center = ttk.LabelFrame(left_frame, text="技術指標最多選擇2個", padding=(20, 5))
        self.left_frame_center.grid(row=1, column=0, padx=(20, 5), pady=(20, 5), sticky="nsew")
        
        # self.ma_var = tk.IntVar()
        # #self.ma_var.set(False)
        # self.macd_var = tk.BooleanVar()
        # self.boo_var = tk.BooleanVar()
        # self.rsi_var = tk.BooleanVar()
        self.check_move = ttk.Checkbutton(
            self.left_frame_center, text="移動平均線", variable=self.ma_var,onvalue=True, offvalue=False,command=lambda:self.toggle_ma(kabu,center_frame)
        )
        self.check_move.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")
        self.check_macd = ttk.Checkbutton(
             self.left_frame_center, text="MACD", variable=self.macd_var,onvalue=True, offvalue=False,command=lambda:self.toggle_macd(kabu,center_frame)
         )
        self.check_macd.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")
        
        self.check_boolean = ttk.Checkbutton(
             self.left_frame_center, text="KDJ", variable=self.kdj_var,onvalue=True, offvalue=False,command=lambda:self.toggle_kdj(kabu,center_frame)
        )
        self.check_boolean.grid(row=2, column=0, padx=5, pady=10, sticky="nsew")
        self.check_xxxx = ttk.Checkbutton(
             self.left_frame_center, text="分價量表", variable=self.volume_var
        )
        self.check_xxxx.grid(row=3, column=0, padx=5, pady=10, sticky="nsew")
        self.ma_var.set(False) 
        self.macd_var.set(False)
        # self.check_xxxx1 = ttk.Radiobutton(
        #      self.left_frame_center, text="XXX1", variable=self.ma_var,value=9
        # )
        # self.check_xxxx1.grid(row=4, column=0, padx=5, pady=10, sticky="nsew")
        #endregion
        #region創建 圓餅圖frame
        self.left_frame_bottom = ttk.LabelFrame(left_frame, text="買?賣?", padding=(20, 5))
        self.left_frame_bottom.grid(row=2, column=0, padx=(20, 5), pady=(10, 5), sticky="nsew")
        self.create_pie_chart(self.left_frame_bottom,buy_sell)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        #endregion
        #region ###################k線圖frame#################
        center_frame = ttk.Frame(detail_window)
        center_frame.grid(row=0, column=1, padx=(20, 5), pady=(10, 5), sticky="nsew")
        # 使用 plotter 模組來繪製圖表
        #data_m,addplot  = m.stock_drop(kabu[0])
        # self.radio_var1 ==3
        self.update_chart(kabu,center_frame)
        #endregion #################k線圖frame#################
        #region####################新聞Paned##################
        # Panedwindow
        self.paned_window = ttk.PanedWindow(detail_window)
        self.paned_window.grid(row=0, column=2, pady=(25, 5), sticky="nsew", rowspan=1)
        # Pane #1
        self.pane_news = ttk.Frame(self.paned_window, padding=10)
        self.paned_window.add(self.pane_news, weight=2) 
        # 縦のスクロール
        self.scrollbar_y_test = ttk.Scrollbar(self.pane_news)
        self.scrollbar_y_test.pack(side="right", fill="y")
        # 水平のスクロール
        self.scrollbar_x_test = ttk.Scrollbar(self.pane_news,orient="horizontal")
        self.scrollbar_x_test.pack(side="bottom", fill="x")
        # Treeview 
        cloumn = ('No','標題','網址')
        self.treeview_new = ttk.Treeview(
            self.pane_news,
            selectmode="browse",
            yscrollcommand=self.scrollbar_y_test.set,
            xscrollcommand=self.scrollbar_x_test.set,
            columns=cloumn,
            height=2,
        )
        self.treeview_new.pack(expand=True, fill="both")
        self.scrollbar_y_test.config(command=self.treeview_new.yview)
        self.scrollbar_x_test.config(command=self.treeview_new.xview)
        # Treeview columns
        self.treeview_new.column('#0', anchor="w", width=1)
        self.treeview_new.column('No', anchor="w", width=30)
        self.treeview_new.column('標題', anchor="w", width=120)
        self.treeview_new.column('網址', anchor="w", width=120)
        # Treeview headings
        self.treeview_new.heading('#0', text="")
        self.treeview_new.heading('No', text="No", anchor="w")
        self.treeview_new.heading('標題', text="標題", anchor="w")
        self.treeview_new.heading('網址', text="網址", anchor="w")
        item = self.treeview_kabu.selection()[0]
        id = self.treeview_kabu.item(item, "values")[0]
        list=m.get_stock_new(id)
        for i in range(len(list.news)):    
            self.treeview_new.insert("", "end", values=(i+1,list.news[i]['title'] , list.news[i]['link']))
        # Sizegrip
        self.sizegrip = ttk.Sizegrip(detail_window)
        self.sizegrip.grid(row=100, column=100, padx=(0, 5), pady=(0, 5))
        # 設定 Treeview 項目點擊事件
        def on_item_click(event):
            """點擊時開啟相關新聞頁面的函數""" 
            item = self.treeview_new.selection()[0]
            url = self.treeview_new.item(item, "values")[2]               
            webbrowser.open(url)
            
        self.treeview_new.bind("<Double-1>", on_item_click)  # 雙擊項目時觸發事件
        #endregion
        #region####################基本面##################
        # Notebook, pane #2
        self.pane_base_info = ttk.Frame(self.paned_window, padding=5)
        self.paned_window.add(self.pane_base_info, weight=1)

        # Notebook, pane #2
        self.notebook = ttk.Notebook(self.pane_base_info)
        self.notebook.pack(fill="both", expand=True)

        # Tab #1
        self.tab_1 = ttk.Frame(self.notebook)
        for index in [0, 1]:
            self.tab_1.columnconfigure(index=index, weight=1)
            self.tab_1.rowconfigure(index=index, weight=1)
        self.notebook.add(self.tab_1, text="Tab 1")
        self.label = ttk.Label(
            self.tab_1,
            text="影片地址",
            justify="center",
        )
        self.label.grid(row=0, column=0, pady=10, columnspan=2)
        # # Scale
        # self.scale = ttk.Scale(
        #     self.tab_1,
        #     from_=100,
        #     to=0,
        #     variable=1
            
        # )
        # self.scale.grid(row=0, column=0, padx=(20, 10), pady=(20, 0), sticky="ew")

        # # Progressbar
        # self.progress = ttk.Progressbar(
        #     self.tab_1, value=0, variable=1, mode="determinate"
        # )
        # self.progress.grid(row=0, column=1, padx=(10, 20), pady=(20, 0), sticky="ew")

        # # Label
        # self.label = ttk.Label(
        #     self.tab_1,
        #     text="Azure theme for ttk",
        #     justify="center",
        #     font=("-size", 15, "-weight", "bold"),
        # )
        # self.label.grid(row=1, column=0, pady=10, columnspan=2)

        # Tab #2
        self.tab_2 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_2, text="Tab 2")

        # Tab #3
        self.tab_3 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_3, text="Tab 3")

        # Sizegrip
        self.sizegrip = ttk.Sizegrip(self)
        self.sizegrip.grid(row=100, column=100, padx=(0, 5), pady=(0, 5))
        #endregion
                       
    def setup_widgets(self):
        """用於主畫面的函數"""
        #region  Radiobutton
        self.check_frame = ttk.LabelFrame(self, text="菜單", padding=(20, 10))
        self.check_frame.grid(
            row=0, column=0, padx=(20, 10), pady=(20, 10), sticky="nsew"
        )
        self.check_youtube = ttk.Radiobutton(
            self.check_frame, text="Youtube影片下載", variable=self.radio_var,value=1,command=lambda:self.changePage(self.widgets_frame_yt)
        )
        self.check_youtube.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")
        self.check_kabu = ttk.Radiobutton(
            self.check_frame, text="股票偵測", variable=self.radio_var,value=2,command=lambda:self.changePage(self.widgets_frame_kabu)
        )
        self.check_kabu.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")
        
        
        
        #endregion
        #region #################Youtube影片下載frame#################
        self.widgets_frame_yt = ttk.Frame(self, padding=(0, 0, 0, 10))
        self.widgets_frame_yt.grid(
            row=0, column=1, padx=10, pady=(30, 10), sticky="nsew", rowspan=3
        )
        self.widgets_frame_yt.columnconfigure(index=0, weight=1)
        self.label = ttk.Label(
            self.widgets_frame_yt,
            text="影片地址",
            justify="center",
        )
        self.label.grid(row=0, column=0, pady=10, columnspan=2)
        self.entry_youtube_url = ttk.Entry(self.widgets_frame_yt)
        self.entry_youtube_url.grid(row=1, column=0, padx=5, pady=(0, 10), sticky="ew")
        self.label = ttk.Label(
            self.widgets_frame_yt,
            text="保存地址",
            justify="center",
        )
        self.label.grid(row=2, column=0, pady=10, columnspan=2)
        self.entry_youtube_folder = ttk.Entry(self.widgets_frame_yt)
        self.entry_youtube_folder.grid(row=3, column=0, padx=5, pady=(0, 10), sticky="ew")
        self.button_folder = ttk.Button(self.widgets_frame_yt, text="打開文件夾",command=self.folderOpen)
        self.button_folder.grid(row=5, column=0, padx=5, pady=10, sticky="nsew")
        self.check_youtube_mp4 = ttk.Radiobutton(
            self.widgets_frame_yt, text="MP3", variable=self.radio_var,value=3
        )
        self.check_youtube_mp4.grid(row=6, column=0, padx=5, pady=10, sticky="nsew")
        self.check_youtube_mp3 = ttk.Radiobutton(
            self.widgets_frame_yt, text="MP4", variable=self.radio_var,value=4
        )
        self.check_youtube_mp3.grid(row=7, column=0, padx=5, pady=10, sticky="nsew")
        self.button_dl = ttk.Button(self.widgets_frame_yt, text="下載開始",command=self.click_youtube)
        self.button_dl.grid(row=8, column=0, padx=5, pady=10, sticky="nsew")      
        # Panedwindow
        self.paned = ttk.PanedWindow(self)
        self.paned.grid(row=0, column=2, pady=(25, 5), sticky="nsew", rowspan=3)
        # Pane #1
        self.pane_1 = ttk.Frame(self.paned, padding=10)
        self.paned.add(self.pane_1, weight=5) 
        # 縦のスクロール
        self.scrollbar_y = ttk.Scrollbar(self.pane_1)
        self.scrollbar_y.pack(side="right", fill="y")
        # 水平のスクロール
        self.scrollbar_x = ttk.Scrollbar(self.pane_1,orient="horizontal")
        self.scrollbar_x.pack(side="bottom", fill="x")
        # Treeview 
        cloumn = ('No','影片名','進度')
        self.treeview_youtube = ttk.Treeview(
            self.pane_1,
            selectmode="browse",
            yscrollcommand=self.scrollbar_y.set,
            xscrollcommand=self.scrollbar_x.set,
            columns=cloumn,
            height=15,
        )
        self.treeview_youtube.pack(expand=True, fill="both")
        self.scrollbar_y.config(command=self.treeview_youtube.yview)
        self.scrollbar_x.config(command=self.treeview_youtube.xview)
        # Treeview columns
        self.treeview_youtube.column('#0', anchor="w", width=1)
        self.treeview_youtube.column('No', anchor="w", width=30)
        self.treeview_youtube.column('影片名', anchor="w", width=120)
        self.treeview_youtube.column('進度', anchor="w", width=120)
        # Treeview headings
        self.treeview_youtube.heading('#0', text="")
        self.treeview_youtube.heading('No', text="No", anchor="w")
        self.treeview_youtube.heading('影片名', text="影片名", anchor="w")
        self.treeview_youtube.heading('進度', text="進度", anchor="w")
        # Sizegrip
        self.sizegrip = ttk.Sizegrip(self)
        self.sizegrip.grid(row=100, column=100, padx=(0, 5), pady=(0, 5))
        #endregion#################Youtube影片下載frame#################
        #region #################股票偵測fram#########################
        self.widgets_frame_kabu = ttk.Frame(self, padding=(0, 0, 0, 10))
        self.widgets_frame_kabu.grid(
            row=0, column=1, padx=10, pady=(30, 10), sticky="nsew", rowspan=3
        )
        self.widgets_frame_kabu.columnconfigure(index=0, weight=1)
        #label
        self.label = ttk.Label(
            self.widgets_frame_kabu,
            text="股票代碼",
            justify="center",
        )
        self.label.grid(row=0, column=0, pady=10, columnspan=2)
        #textbox
        self.entry_kabu = ttk.Entry(self.widgets_frame_kabu)
        self.entry_kabu.grid(row=1, column=0, padx=5, pady=(0, 10), sticky="ew")
        #textbox
        # self.entry_kabu_buy_1 = ttk.Entry(self.widgets_frame_kabu)
        # self.entry_kabu_buy_1.grid(row=3, column=0, padx=5, pady=(0, 10), sticky="ew")
        # self.entry_kabu_buy_2 = ttk.Entry(self.widgets_frame_kabu)
        # self.entry_kabu_buy_2.grid(row=4, column=0, padx=5, pady=(0, 10), sticky="ew")
        # self.entry_kabu_buy_3 = ttk.Entry(self.widgets_frame_kabu)
        # self.entry_kabu_buy_3.grid(row=5, column=0, padx=5, pady=(0, 10), sticky="ew")
        #button
        self.button_kabu = ttk.Button(self.widgets_frame_kabu, text="查詢",command=self.click_kabu)
        self.button_kabu.grid(row=6, column=0, padx=5, pady=10, sticky="nsew")
        #button
        self.button_kabu_1 = ttk.Button(self.widgets_frame_kabu, text="每日回報率",command=self.click_ROI)
        self.button_kabu_1.grid(row=7, column=0, padx=5, pady=10, sticky="nsew")
        
        # Treeview
        cloumn_kabu = ('代號','股票名','即時股價','1年最高','1年最低')
        self.treeview_kabu = ttk.Treeview(
            self.pane_1,
            selectmode="browse",
            yscrollcommand=self.scrollbar_y.set,
            xscrollcommand=self.scrollbar_x.set,
            columns=cloumn_kabu,
            height=15,
        )
        self.treeview_kabu.pack(expand=True, fill="both")
        self.scrollbar_y.config(command=self.treeview_kabu.yview)
        self.scrollbar_x.config(command=self.treeview_kabu.xview)
        # Treeview columns
        self.treeview_kabu.column('#0', anchor="w", width=1)
        self.treeview_kabu.column('代號', anchor="w", width=60)
        self.treeview_kabu.column('股票名', anchor="w", width=120)
        self.treeview_kabu.column('即時股價', anchor="w", width=60)
        self.treeview_kabu.column('1年最高', anchor="w", width=60)
        self.treeview_kabu.column('1年最低', anchor="w", width=60)
        # Treeview headings
        self.treeview_kabu.heading('#0', text="")
        self.treeview_kabu.heading('代號', text="代號", anchor="w")
        self.treeview_kabu.heading('股票名', text="股票名", anchor="w")
        self.treeview_kabu.heading('即時股價', text="即時股價", anchor="w")
        self.treeview_kabu.heading('1年最高', text="1年最高", anchor="w")
        self.treeview_kabu.heading('1年最低', text="1年最低", anchor="w")
        
        #endregion#################股票偵測fram#########################       
        
        self.treeview_kabu.pack_forget()    
        self.widgets_frame_yt.tkraise()

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    root.title("")
    # Simply set the theme
    dir_path = os.path.dirname(os.path.realpath(__file__))
    root.tk.call('source', os.path.join(dir_path, 'azure.tcl'))
    #root.tk.call("source", "azure.tcl")
    root.tk.call("set_theme", "dark")
    app = App(root)
    app.pack(fill="both", expand=True)
    # Set a minsize for the window, and place it in the middle
    root.update()
    root.minsize(root.winfo_width(), root.winfo_height())
    x_cordinate = int((root.winfo_screenwidth() / 2) - (root.winfo_width() / 2))
    y_cordinate = int((root.winfo_screenheight() / 2) - (root.winfo_height() / 2))
    root.geometry("+{}+{}".format(x_cordinate, y_cordinate-20))
    root.mainloop()
