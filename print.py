import subprocess
import time
import ctypes
import sys
import tkinter as tk
from tkinter import messagebox

service_name = "Adicon.YLIMS.DeviceService"

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def check_service_status(service_name):
    try:
        result = subprocess.run(["sc", "query", service_name], capture_output=True, text=True, check=True)
        if "RUNNING" in result.stdout:
            return "RUNNING"
        elif "STOPPED" in result.stdout:
            return "STOPPED"
        else:
            return "UNKNOWN"
    except subprocess.CalledProcessError:
        return "UNKNOWN"

def restart_service(service_name):
    try:
        status = check_service_status(service_name)
        if status == "RUNNING":
            subprocess.run(["net", "stop", service_name], check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            time.sleep(1)
            subprocess.run(["net", "start", service_name], check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            messagebox.showinfo("提示", f"{service_name} 服务已成功重新启动！")
        elif status == "STOPPED":
            subprocess.run(["net", "start", service_name], check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            time.sleep(1)
            subprocess.run(["net", "stop", service_name], check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            time.sleep(1)
            subprocess.run(["net", "start", service_name], check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            messagebox.showinfo("提示", f"{service_name} 服务已成功重新启动！")
        else:
            messagebox.showerror("错误", f"无法获取 {service_name} 服务的状态。")
    except subprocess.CalledProcessError:
        messagebox.showerror("错误", f"无法停止、启动或重新启动 {service_name} 服务。")
        time.sleep(1)

# 直接调用重新启动服务函数
restart_service(service_name)

