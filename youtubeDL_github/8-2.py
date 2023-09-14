import tkinter as tk
def check_pw():
    if pwvar.get() == 'flag':
        msgvar.set('pw is good')
    else:
        msgvar.set('pw is error')
windows=tk.Tk()
lb_pw=tk.Label(windows,text='please input pw')
lb_pw.pack()
pwvar = tk.StringVar()
entry = tk.Entry(windows,width=15,textvariable=pwvar,show='*')
entry.pack()
btn = tk.Button(windows,text='test',command=check_pw)
btn.pack()
msgvar = tk.StringVar()
lb_msg = tk.Label(windows,textvariable=msgvar)
lb_msg.pack()
windows.mainloop()
