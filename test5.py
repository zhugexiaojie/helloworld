import tkinter as tk
from tkinter import simpledialog, messagebox
import pyodbc

# 数据库连接信息字典，存储不同区域的连接信息
database_info = {
    '济南': {'server': '10.0.0.200', 'database': 'lisdb', 'uid': 'lisuser', 'pwd': 'lisuser'},
    '青岛': {'server': '10.0.0.201', 'database': 'lisdb', 'uid': 'lisuser', 'pwd': 'lisuser'},
    '杭州': {'server': '192.168.31.251', 'database': 'lisdb', 'uid': 'lisuser', 'pwd': 'lisuser'}, 
    '北京': {'server': '10.3.0.3', 'database': 'lisdb', 'uid': 'lisuser', 'pwd': 'lisuser'},
    '临沂': {'server': '10.39.1.200', 'database': 'lisdb', 'uid': 'lisuser', 'pwd': 'lisuser'},
    '石家庄': {'server': '10.40.1.11', 'database': 'lisdb', 'uid': 'lisuser', 'pwd': 'bBh2bZkdoel3'},
    # 添加其他区域的连接信息
}

def unlock_account(db_type, selected_db):
    account = simpledialog.askstring(f"请输入{selected_db}账号", f"请输入{selected_db}账号")
    if account:
        if selected_db in database_info:
            region_data = database_info[selected_db]
            
            try:
                # 连接数据库...
                # 查询和更新逻辑...
                pass
            except pyodbc.Error as e:
                messagebox.showerror('数据库连接或查询错误', f'错误：{e}')
        else:
            messagebox.showerror("无效的区域", "请选择有效的区域")
    else:
        messagebox.showwarning("请输入正确的账号", "请输入正确的账号")

def on_region_selected(event):
    selected_db = selected_region.get()
    if selected_db:
        show_unlock_buttons(selected_db)

def show_unlock_buttons(selected_db):
    new_window = tk.Toplevel(window)
    new_window.title(f"{selected_db}解锁")
    new_window.geometry("300x150")

    lims_button = tk.Button(new_window, text="lims解锁", command=lambda: unlock_account('lims', selected_db), width=12, height=2)
    lims_button.pack(pady=10)

    lis_button = tk.Button(new_window, text="lis解锁", command=lambda: unlock_account('lis', selected_db), width=12, height=2)
    lis_button.pack()

# 创建主窗口
window = tk.Tk()
window.title("账号解锁程序")
window.geometry("400x150")  # 设置主窗口的大小

# 创建提示标签
prompt_label = tk.Label(window, text="请选择区域:", font=("Helvetica", 12))
prompt_label.pack(pady=10)

# 创建区域选择下拉菜单
selected_region = tk.StringVar()  # 存储用户选择的区域
region_menu = tk.OptionMenu(window, selected_region, *database_info.keys())
region_menu.config(font=("Helvetica", 12))
region_menu.pack(pady=5)

# 绑定选择区域事件，当选择区域后自动弹出窗口
selected_region.trace("w", lambda *args: on_region_selected(args))

# 运行主循环
window.mainloop()
