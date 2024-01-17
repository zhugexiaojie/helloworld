import pyperclip

def add_underline_subscript(number):
    formatted_number = number.replace("\\0332", "₉")
    pyperclip.copy(formatted_number)
    print("已复制带下横杠的数字到剪贴板：" + formatted_number)

if __name__ == '__main__':
    input_number = input("请输入一个数字：")
    add_underline_subscript(input_number)
