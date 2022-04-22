import os
import random


import xlrd


class Common:

    # 从用户表中随机选取一个账户
    def random_account(self):
        book = xlrd.open_workbook(r"D:\测试工作文件夹\okmarts\O&Kmark\okmarts账户.xls")
        sh = book.sheet_by_name('Sheet1')
        nrows = sh.nrows  # 获取行数
        random_row = random.randint(1, nrows - 1)  # 随机行数
        userAgent = sh.cell_value(rowx=random_row, colx=0)
        password = sh.cell_value(rowx=random_row, colx=1)
        return userAgent, password


    def random_email_account(self):
        account_li = "a8837749" + random.choice(['20','19','18','17','16'])+'@163.com'
        print(account_li)
        return account_li



    # 关闭所有浏览器
    def close_browser(self):
        cmd = 'TASKKILL /F /IM chrome.exe /T'
        os.system(cmd)

if __name__ == '__main__':
    a = Common()
    a.random_email_account()