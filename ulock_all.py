import tkinter as tk
from tkinter import simpledialog, messagebox
from tkinter import ttk
import pyodbc

# 默认数据库连接信息
default_db_info = {
    'ip': '10.0.0.200',
    'database': 'lisdb',
    'user': 'lisuser',
    'password': 'lisuser'
}

def update_db_info(region):
    # 根据选择的区域更新数据库连接信息
    # 添加更多区域的数据库连接信息
    region_db_info = {
        '济南': {'ip': '10.0.0.200', 'database': 'lisdb', 'user': 'lisuser', 'password': 'lisuser'},
        '北京': {'ip': '10.3.0.3', 'database': 'lisdb', 'user': 'lisuser', 'password': 'lisuser'},
        '成都': {'ip': '10.11.0.5', 'database': 'lisdb', 'user': 'lisuser', 'password': 'lisuser'},
        '福州': {'ip': '10.5.0.1', 'database': 'lisdb', 'user': 'lisuser', 'password': 'lisuser'},
        '广州': {'ip': '10.13.1.10', 'database': 'lisdb', 'user': 'lisuser', 'password': 'lisuser'},
        '贵阳': {'ip': '10.23.1.2', 'database': 'lisdb', 'user': 'lisuser', 'password': 'lisuser'},
        '合肥': {'ip': '10.2.0.188', 'database': 'lisdb', 'user': 'lisuser', 'password': 'lisuser'},
        '黑龙江': {'ip': '10.29.1.11', 'database': 'lisdb', 'user': 'lisuser', 'password': 'lisuser'},
        '临沂': {'ip': '10.39.1.200', 'database': 'lisdb', 'user': 'lisuser', 'password': 'lisuser'},
        '南昌': {'ip': '10.4.0.3', 'database': 'lisdb', 'user': 'lisuser', 'password': 'lisuser'},
        '南京': {'ip': '10.8.0.250', 'database': 'lisdb', 'user': 'lisuser', 'password': 'lisuser'},
        '南宁': {'ip': '10.19.3.6', 'database': 'lisdb', 'user': 'lisuser', 'password': 'lisuser'},
        '青岛': {'ip': '10.20.1.3', 'database': 'lisdb', 'user': 'lisuser', 'password': 'lisuser'},
        '衢州': {'ip': '10.24.1.251', 'database': 'lisdb', 'user': 'lisuser', 'password': 'lisuser'},
        '三明': {'ip': '10.16.0.10', 'database': 'lisdb', 'user': 'lisuser', 'password': 'lisuser'},
        '厦门': {'ip': '10.27.1.5', 'database': 'lisdb', 'user': 'lisuser', 'password': 'lisuser'},
        '商丘': {'ip': '10.33.1.130', 'database': 'lisdb', 'user': 'lisuser', 'password': 'lisuser'},
        '上海': {'ip': '172.20.220.88', 'database': 'lisdb', 'user': 'lisuser', 'password': 'lisuser'},
        '上饶': {'ip': '10.25.0.3', 'database': 'lisdb', 'user': 'lisuser', 'password': 'lisuser'},
        '深圳': {'ip': '10.21.1.12', 'database': 'lisdb', 'user': 'lisuser', 'password': 'lisuser'},
        '沈阳': {'ip': '10.10.0.10', 'database': 'lisdb', 'user': 'lisuser', 'password': 'lisuser'},
        '天津': {'ip': '10.15.0.5', 'database': 'lisdb', 'user': 'lisuser', 'password': 'lisuser'},
        '武汉': {'ip': '10.7.0.251', 'database': 'lisdb', 'user': 'lisuser', 'password': 'lisuser'},
        '西安': {'ip': '10.17.0.10', 'database': 'lisdb', 'user': 'lisuser', 'password': 'lisuser'},
        '云南': {'ip': '10.14.0.251', 'database': 'lisdb', 'user': 'lisuser', 'password': 'lisuser'},
        '长春': {'ip': '10.6.0.251', 'database': 'lisdb', 'user': 'lisuser', 'password': 'lisuser'},
        '长沙': {'ip': '10.9.0.5', 'database': 'lisdb', 'user': 'lisuser', 'password': 'lisuser'},
        '郑州': {'ip': '10.12.3.200', 'database': 'lisdb', 'user': 'lisuser', 'password': 'lisuser'},
        '重庆': {'ip': '10.18.5.20', 'database': 'lisdb', 'user': 'lisuser', 'password': 'lisuser'},
        '石家庄': {'ip': '10.40.1.11', 'database': 'lisdb', 'user': 'lisuser', 'password': 'bBh2bZkdoel3'},
    }

    default_db_info.update(region_db_info.get(region, {}))

def unlock_account(option, sub_window):
    def unlock():
        account = simpledialog.askstring(f"请输入{option}账号", f"请输入{option}账号", parent=sub_window)
        if account:
            query = ""
            update_query = ""

            if option == "lims":
                query = f"SELECT Userid FROM LIS.dbo.Users WHERE Userid = '{account}' AND IsValid <> 0"
                update_query = f"UPDATE LIS.dbo.Users SET locked = NULL WHERE Userid = '{account}' AND IsValid <> 0"
            elif option == "lis":
                query = f"SELECT logid FROM lisdb..xt_user WHERE logid = '{account}' AND status <> 1"
                update_query = f"UPDATE lisdb..xt_user SET status = 0 WHERE logid = '{account}' AND status <> 1"

            conn = pyodbc.connect(
                f"DRIVER={{SQL Server}};SERVER={default_db_info['ip']};"
                f"DATABASE={default_db_info['database']};"
                f"UID={default_db_info['user']};PWD={default_db_info['password']}"
            )
            cursor = conn.cursor()

            # 查询账号是否存在
            cursor.execute(query)
            result = cursor.fetchone()

            if result:
                # 执行更新操作
                cursor.execute(update_query)
                conn.commit()

                messagebox.showinfo("解锁成功", "已解锁")
            else:
                messagebox.showwarning("账号不存在", "此账号不存在")

            cursor.close()
            conn.close()

            # 关闭子窗口
            sub_window.destroy()

    return unlock

def show_unlock_options():
    selected_region = region_var.get()
    update_db_info(selected_region)

    sub_window = tk.Toplevel(window)
    sub_window.title("解锁")
    sub_window.geometry("300x150")

    # 解锁按钮
    lis_button = tk.Button(sub_window, text="lis解锁", command=unlock_account("lis", sub_window))
    lims_button = tk.Button(sub_window, text="lims解锁", command=unlock_account("lims", sub_window))

    lis_button.place(relx=0.3, rely=0.4, anchor="center")
    lims_button.place(relx=0.7, rely=0.4, anchor="center")

# 创建主窗口
window = tk.Tk()
window.title("账号解锁程序")
window.geometry("400x300")
window.configure(bg="white")  # 设置窗口背景为白色

# 将窗口放置在屏幕中央
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x_coordinate = (screen_width - 400) // 2
y_coordinate = (screen_height - 300) // 2
window.geometry(f"400x300+{x_coordinate}+{y_coordinate}")

# 使用ttk模块创建带样式的下拉菜单
style = ttk.Style()
style.theme_use('clam')  # 使用clam主题，也可以尝试其他主题

region_var = tk.StringVar(window)
regions = ['济南', '北京', '成都', '福州', '广州', '贵阳', '合肥', '黑龙江', '临沂', '南昌', '南京', '南宁',
           '青岛', '衢州', '三明', '厦门', '商丘', '上海', '上饶', '深圳', '沈阳', '天津', '武汉', '西安', '云南', '长春', '长沙', '郑州', '重庆', '石家庄']
region_var.set(regions[0])

region_menu = ttk.Combobox(window, textvariable=region_var, values=regions, state="readonly", style="TCombobox")
region_menu.place(relx=0.5, rely=0.4, anchor="center")

# 解锁按钮
unlock_button = tk.Button(window, text="选择区域并解锁", command=show_unlock_options, width=15, height=2)
unlock_button.place(relx=0.5, rely=0.6, anchor="center")

# 运行主循环
window.mainloop()
