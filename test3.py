import tkinter as tk
from tkinter import messagebox
import pyodbc

def execute_query():
    customer_id = entry.get()

    # 连接数据库
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER=10.0.0.200;DATABASE=lisdb;UID=lisuser;PWD=lisuser')

    # 执行查询
    cursor = conn.cursor()
    query = f"SELECT B.DH, b.mc, lisdb.dbo.F_Decrypt(b.password2) FROM lisdb..xt_yymc_print b WHERE DH IN ('{customer_id}')"
    cursor.execute(query)
    result = cursor.fetchone()

    # 关闭数据库连接
    conn.close()

    # 检查查询结果
    if result is not None:
        # 显示密码
        password = result[2]
        messagebox.showinfo('密码', f'密码为：{password}')
    else:
        # 提示查询无结果
        messagebox.showinfo('查询无结果', '请检查是否输入有误或该客户是否已启用')

# 创建主窗口
window = tk.Tk()
window.title('查询密码')
window.geometry('300x100')  # 设置窗口尺寸为500x300像素

# 创建标签和输入框
label = tk.Label(window, text='请输入客户代号：')
label.pack()

entry = tk.Entry(window)
entry.pack()

# 创建按钮
button = tk.Button(window, text='确定', command=execute_query)
button.pack()

# 运行主循环
window.mainloop()
