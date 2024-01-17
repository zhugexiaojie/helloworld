import tkinter as tk
import pyodbc
import pandas as pd
from tkinter import messagebox, filedialog

# 数据库连接信息
server = '10.0.0.200'
database = 'lisdb'
username = 'lisuser'
password = 'lisuser'

# 创建窗口
window = tk.Tk()
window.title('在职离职人员查询')
window.geometry('400x150')

# 创建标签和选择框
label = tk.Label(window, text='请选择查询类型：')
label.pack()

v = tk.StringVar()
r1 = tk.Radiobutton(window, text='在职', variable=v, value='1')
r1.pack()

r2 = tk.Radiobutton(window, text='离职', variable=v, value='2')
r2.pack()

# 查询函数
def query():
    # 根据选择的查询类型，构造SQL语句
    if v.get() == '1':
        sql = "select logid as 'lis账号', username as '姓名', status as '状态', adiconuser as '工号', beizhu as '备注' from xt_user where status in (0, 2)"
    else:
        sql = "select logid as 'lis账号', username as '姓名', status as '状态', adiconuser as '工号', beizhu as '备注' from xt_user where status = 1"
    
    # 连接数据库，执行查询
    conn = pyodbc.connect(f"Driver={{SQL Server}};Server={server};Database={database};UID={username};PWD={password}")
    data = pd.read_sql(sql, conn)
    
    # 弹出文件保存对话框，将查询结果导出为Excel文件
    file_path = filedialog.asksaveasfilename(defaultextension='.xlsx')
    if file_path:
        data.to_excel(file_path, index=False)
        messagebox.showinfo('提示', '导出成功！')
    
    # 关闭数据库连接
    conn.close()

# 创建按钮
button = tk.Button(window, text='查询', command=query)
button.pack()

# 进入消息循环
window.mainloop()