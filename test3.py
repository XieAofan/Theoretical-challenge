import tkinter as tk
from tkinter import messagebox

def login():
    username = entry_username.get()
    password = entry_password.get()
    if username == "admin" and password == "password":
        messagebox.showinfo("登录成功", "欢迎回来，{}!".format(username))
    else:
        messagebox.showerror("登录失败", "用户名或密码错误")

# 创建主窗口
root = tk.Tk()
root.title("登录界面")
root.geometry("300x200")
root.configure(bg="#f0f0f0")

# 用户名标签和输入框
label_username = tk.Label(root, text="用户名:", bg="#f0f0f0")
label_username.pack(pady=5)
entry_username = tk.Entry(root)
entry_username.pack(pady=5)

# 密码标签和输入框
label_password = tk.Label(root, text="密码:", bg="#f0f0f0")
label_password.pack(pady=5)
entry_password = tk.Entry(root, show="*")
entry_password.pack(pady=5)

# 登录按钮
button_login = tk.Button(root, text="登录", command=login, bg="#4CAF50", fg="white", activebackground="#45a049")
button_login.pack(pady=20)

# 运行主循环
root.mainloop()