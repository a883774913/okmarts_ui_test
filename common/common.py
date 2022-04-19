import random

import xlrd


class Common:

    # 从用户表中随机选取一个账户
    def random_account(self):
        book = xlrd.open_workbook(r"C:\Users\admin\Desktop\okmarts\O&Kmark\okmarts账户.xls")
        sh = book.sheet_by_name('Sheet1')
        nrows = sh.nrows  # 获取行数
        random_row = random.randint(1, nrows - 1)  # 随机行数
        userAgent = sh.cell_value(rowx=random_row, colx=0)
        password = sh.cell_value(rowx=random_row, colx=1)
        return userAgent, password
