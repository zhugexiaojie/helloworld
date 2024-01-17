import os
import tkinter as tk


class MicrobialEcologyApp:
    def __init__(self, root):
        self.root = root
        self.root.title('阴道微生态切换工具')
        self.root.geometry('300x200')

        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=20)

        self.button1 = tk.Button(self.frame, text="切换阴道微生态为新lis", command=self.switch_to_new_lis)
        self.button1.pack(pady=5)

        self.button2 = tk.Button(self.frame, text="还原阴道微生态为老lis", command=self.switch_to_old_lis, state=tk.DISABLED)
        self.button2.pack(pady=5)

    def switch_to_new_lis(self):
        path = r'D:\Comet800Cro24图像处理系统\xml_config'

        if os.path.exists(os.path.join(path, 'XML_Config.xml')):
            os.rename(os.path.join(path, 'XML_Config.xml'), os.path.join(path, 'XML_Config old.xml'))
        if os.path.exists(os.path.join(path, 'XML_Config new.xml')):
            os.rename(os.path.join(path, 'XML_Config new.xml'), os.path.join(path, 'XML_Config.xml'))

        self.button1.config(state=tk.DISABLED)
        self.button2.config(state=tk.NORMAL)

    def switch_to_old_lis(self):
        path = r'D:\Comet800Cro24图像处理系统\xml_config'

        if os.path.exists(os.path.join(path, 'XML_Config.xml')):
            os.rename(os.path.join(path, 'XML_Config.xml'), os.path.join(path, 'XML_Config new.xml'))
        if os.path.exists(os.path.join(path, 'XML_Config old.xml')):
            os.rename(os.path.join(path, 'XML_Config old.xml'), os.path.join(path, 'XML_Config.xml'))

        self.button1.config(state=tk.NORMAL)
        self.button2.config(state=tk.DISABLED)


if __name__ == '__main__':
    root = tk.Tk()
    app = MicrobialEcologyApp(root)
    root.mainloop()
