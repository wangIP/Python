import ytube_module as m
import tkinter as tk
from tkinter import messagebox
from pytube import YouTube  
import threading

def click_func():
    url= entryvar.get()
    # try:
    #     YouTube(url)
    # except:
    #     messagebox.showerror('error','error msg')
    #     return
    urls = m.get_urls(url)
    if urls and messagebox.askyesno('確認方塊', 
            '是否下載清單內所有影片？(選擇 否(N) 則下載單一影片)'):
        print('start')
        for u in urls:
            threading.Thread(target=m.start_dload,args=(u,listbox)).start()
    else:
            threading.Thread(target = m.start_dload, 
                             args=(url, listbox)).start()  

windows = tk.Tk()
windows.title('youtubeDL')
windows.geometry('640x500')

#frame create
frame_area = tk.Frame(windows,bg='#BAD3FF',width=640,height=120)
frame_area.pack()

#lable create
lb = tk.Label(frame_area,text='pls input youtube URL',bg='red',fg='white',font=('Meiryo UI',12,'bold'))
lb.place(rely=0.25,relx=0.5,anchor='center')

#entry textbox create
entryvar = tk.StringVar()
entry_textbox = tk.Entry(frame_area,textvariable=entryvar,width=50)
entry_textbox.place(rely=0.5,relx=0.5,anchor='center')

#button create

btn = tk.Button(frame_area,text='video DL',command=click_func,bg='#FFD700',fg='Black',font=('Meiryo UI',10,'bold'))
btn.place(rely=0.5,relx=0.85, anchor='center')

#frame create
dload_fm = tk.Frame(windows,bg='#BAD3FF',width=640,height=480-120)
dload_fm.pack()

#lable create
lb = tk.Label(dload_fm,text='DL status',fg='black',font=('Meiryo UI',14,'bold'))
lb.place(rely=0.1,relx=0.5,anchor='center')

#listbox create
listbox = tk.Listbox(dload_fm,width=65,height=15)
listbox.place(rely=0.5,relx=0.5,anchor='center')

#scrollbar create
sbar = tk.Scrollbar(dload_fm)
sbar.place(rely=0.5,relx=0.87,anchor='center',relheight=0.7)

#scrollbar build with listbox
listbox.config(yscrollcommand=sbar.set)
sbar.config(command=listbox.yview)







windows.mainloop()