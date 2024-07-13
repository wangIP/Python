def sns_edit_click(event):
            """點擊時彈出新窗口""" 
            root_sns = tk.Tk()
            root_sns.title("編輯內容")
            root_sns.tk.call("source", "azure.tcl")
            root_sns.tk.call("set_theme", "dark")
            x_cordinate = int((root.winfo_screenwidth() / 2) - (root.winfo_width() / 2))
            y_cordinate = int((root.winfo_screenheight() / 2) - (root.winfo_height() / 2))
            root_sns.geometry("+{}+{}".format(x_cordinate, y_cordinate-20))
            #root_sns.geometry("430x600")
            sns_frame = ttk.Frame(root_sns)
            sns_frame.grid(
                row=0, column=2, padx=10, pady=(30, 10), sticky="nsew", rowspan=1
            )
            sns_frame.columnconfigure(index=0, weight=1)
            label = ttk.Label(
                sns_frame,
                text="標題",
                justify="center",
            )
            label.grid(row=1, column=0, pady=10, columnspan=1)
            entry_sns_title = ttk.Entry(sns_frame,width=40)
            entry_sns_title.grid(row=2, column=1, padx=5, pady=(0, 10), sticky="ew")
            
            sns_frame_text = ttk.Frame(root_sns)
            sns_frame_text.grid(
                row=1, column=2, padx=10, pady=(30, 10), sticky="nsew", rowspan=2
            )
            sns_frame_text.columnconfigure(index=0, weight=1)
            
            label = ttk.Label(
                sns_frame_text,
                text="內容",
                justify="center",
            )
            label.grid(row=1, column=0, pady=10, columnspan=1)
            entry_sns_text = tk.Text(sns_frame_text,width=40,height=10)
            entry_sns_text.grid(row=2, column=1, padx=5, pady=(0, 10), sticky="ew")

            def folderOpen():
                dir = 'D:'
                fld = filedialog.askdirectory(initialdir = dir) 
                entry_sns_photo.insert(0,fld)
            
            label = ttk.Label(
                sns_frame_text,
                text="上傳照片",
                justify="center",
            )
            label.grid(row=3, column=0, pady=10, columnspan=1)
            entry_sns_photo = ttk.Entry(sns_frame_text)
            entry_sns_photo.grid(row=4, column=1, padx=5, pady=(0, 10), sticky="ew")
            button_photo = ttk.Button(sns_frame_text, text="打開文件夾",command=folderOpen)
            button_photo.grid(row=4, column=0, padx=5, pady=10, sticky="nsew")
            button_kakute = ttk.Button(sns_frame_text, text="確定",command=folderOpen)
            button_kakute.grid(row=5, column=0, padx=5, pady=10, sticky="nsew")
            button_chenll = ttk.Button(sns_frame_text, text="取消",command=folderOpen)
            button_chenll.grid(row=5, column=1, padx=5, pady=10, sticky="nsew")