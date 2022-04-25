import os
import random
import time

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
        account_li = "a8837749" + random.choice(['20', '19', '18', '17', '16']) + '@163.com'
        print(account_li)
        return account_li

    # 关闭所有浏览器
    def close_browser(self):
        cmd = 'TASKKILL /F /IM chrome.exe /T'
        os.system(cmd)

    def logo(self,driver,useraccount,password):
        """
        登录页面进行登录，输入账户密码点击登录
        :param driver: 驱动
        :param useraccount: 账户
        :param password: 密码
        :return:
        """
        driver.find_element(by='id', value='horizontal_login_userAccount').send_keys(useraccount)  # 登录
        driver.find_element(by='id', value='horizontal_login_password').send_keys(password)
        driver.find_element(by='class name', value='atn-btn-orange.ant-btn.ant-btn-lg.ant-btn-block').click()
        time.sleep(2)

    def Restore_environment(self, dr):
        """
        检测是否为登录状态，如果登录推出登录状态，如果未登录则PASS
        :param dr:  驱动
        :return:
        """
        print(dr.find_element(by='xpath', value='//*[@id="app"]/div/div[1]/div/div[2]/div[3]/div[1]').text)
        if dr.find_element(by='xpath',
                           value='//*[@id="app"]/div/div[1]/div/div[2]/div[3]/div[1]').text == 'Login':  # 如果为login 则为未登录状态
            pass
        else:
            dr.find_element(by='xpath',
                            value='//*[@id="app"]/div/div[1]/div/div[2]/div[3]/div[1]').click()  # 点击按钮进入个人中心
            time.sleep(1)
            dr.find_element(by='class name', value='login-out.text-white').click()  # 点击注销
            time.sleep(0.5)
            dr.find_element(by='class name', value='ant-btn.ant-btn-primary.ant-btn-sm').click()  # 点击确认
            time.sleep(0.5)

if __name__ == '__main__':
    a = Common()
    a.random_email_account()
