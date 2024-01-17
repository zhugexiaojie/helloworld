import tkinter as tk
from tkinter import simpledialog, messagebox
import pyodbc


def unlock_lims():
    account = simpledialog.askstring("请输入lims账号", "请输入lims账号", parent=window)
    if account:
        # 连接数据库
        conn = pyodbc.connect("DRIVER={SQL Server};SERVER=10.0.0.200;DATABASE=lisdb;UID=lisuser;PWD=lisuser")
        cursor = conn.cursor()

        # 查询账号是否存在
        query = f"SELECT Userid FROM LIS.dbo.Users WHERE Userid = '{account}' AND IsValid <> 0"
        cursor.execute(query)
        result = cursor.fetchone()

        if result:
            # 执行更新操作
            update_query = f"UPDATE LIS.dbo.Users SET locked = NULL WHERE Userid = '{account}' AND IsValid <> 0"
            cursor.execute(update_query)
            conn.commit()

            messagebox.showinfo("解锁成功", "已解锁")
        else:
            messagebox.showwarning("账号不存在", "此账号不存在")

        # 关闭数据库连接
        cursor.close()
        conn.close()
    else:
        messagebox.showwarning("请输入正确的账号", "请输入正确的账号")


def unlock_lis():
    account = simpledialog.askstring("请输入lis账号", "请输入lis账号", parent=window)
    if account:
        # 连接数据库
        conn = pyodbc.connect("DRIVER={SQL Server};SERVER=10.0.0.200;DATABASE=lisdb;UID=lisuser;PWD=lisuser")
        cursor = conn.cursor()

        # 查询账号是否存在
        query = f"SELECT logid FROM lisdb..xt_user WHERE logid = '{account}' AND status <> 1"
        cursor.execute(query)
        result = cursor.fetchone()

        if result:
            # 执行更新操作
            update_query = f"UPDATE lisdb..xt_user SET status = 0 WHERE logid = '{account}' AND status <> 1"
            cursor.execute(update_query)
            conn.commit()

            messagebox.showinfo("解锁成功", "已解锁")
        else:
            messagebox.showwarning("账号不存在", "此账号不存在")

        # 关闭数据库连接
        cursor.close()
        conn.close()
    else:
        messagebox.showwarning("请输入正确的账号", "请输入正确的账号")


# 创建主窗口
window = tk.Tk()
window.title("账号解锁程序")

# 设置主窗口的大小
window.geometry("400x300")

# 计算按钮的大小和位置
button_width = 8
button_height = 2
button_x = (window.winfo_width() - button_width) // 2
button_y = (window.winfo_height() - button_height) // 2

# 创建按钮
lims_button = tk.Button(window, text="lims解锁", command=unlock_lims, width=button_width, height=button_height)
lims_button.place(relx=0.5, rely=0.4, anchor="center")

lis_button = tk.Button(window, text="lis解锁", command=unlock_lis, width=button_width, height=button_height)
lis_button.place(relx=0.5, rely=0.6, anchor="center")

# 运行主循环
window.mainloop()