
"""
获取验证码 163 邮箱
"""

import re
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By


class Get_Code:

    # def change_pwd(self,password,newpassword):
    #
    #     driver = webdriver.Chrome()  # 打开浏览器
    #     driver.get("http://18.118.13.94:81/index")
    #     driver.maximize_window()  # 窗口最大化
    #     time.sleep(0.5)
    #     driver.find_element(by=By.XPATH, value="/html/body/div/div/div[1]/div/div[2]/div[3]/div[1]").click()  # 点击登录
    #     time.sleep(1)
    #     driver.find_element(by=By.ID, value="horizontal_login_userAccount").send_keys("selenium3366@163.com")  # 输入登录账户
    #     driver.find_element(by=By.ID, value="horizontal_login_password").send_keys(password)  # 输入登录密码
    #     driver.find_element(by=By.CLASS_NAME, value="atn-btn-orange.ant-btn.ant-btn-lg.ant-btn-block").click()  # 点击登录
    #     time.sleep(2)
    #     driver.find_element(by=By.XPATH,
    #                         value="""//*[@id="app"]/div/div[1]/div/div[2]/div[3]/div[1]""").click()  # 点击头像进入个人中心
    #     time.sleep(2)
    #     driver.find_element(by=By.XPATH,
    #                         value="""//*[@id="app"]/div/div[2]/div[1]/div[2]/div[3]""").click()  # 点击change_password
    #     time.sleep(1)
    #     driver.find_element(by=By.XPATH, value="""//*[@id="horizontal_login_newPassword"]""").send_keys(
    #         newpassword)  # 输入新密码
    #     driver.find_element(by=By.XPATH,
    #                         value="""//*[@id="app"]/div/div/div[2]/form/div[2]/div/div/span/div/div[2]/a""").click()  # 点击发送验证码
    #     time.sleep(8)  # 等待验证码发送到该邮箱
    #
    #     self.wangyi(username="selenium3366", password="Qwe3541118", name="okmarket账户信息更改")  # 调用方法获取验证码
    #
    #     driver.find_element(by=By.XPATH, value=
    #     "/html/body/div[1]/div/div/div[2]/form/div[2]/div/div/span/div/div[1]/input").send_keys(
    #         code[0])  # 输入验证码
    #     time.sleep(0.5)
    #     driver.find_element(by=By.XPATH, value=
    #     """/html/body/div[1]/div/div/div[2]/form/div[3]/div/div/span/button""").click()  # 点击按钮
    #     time.sleep(1)
    #     text = driver.find_element(by=By.XPATH, value="""/html/body/div[2]/span/div/div/div/span""").text
    #     print(text)
    #     try:
    #         assert text == "password update success"        #断言
    #         print("修改密码成功")
    #     except:
    #         print("修改失败")

    def __init__(self):
        self.dr = webdriver.Edge()  # 打开另一个浏览器

    def wangyi(self, username, password, name, no:int):

        """
        网易邮箱获取验证码
        :param username: 邮箱账户
        :param password: 邮箱密码
        :param name:  发件人 hydraulic
        :param no : 第几封排序邮件 no>=1
        :return:
        """
        option = webdriver.ChromeOptions()
        option.add_experimental_option("detach", True)

        self.dr.maximize_window()  # 窗口最大化
        self.dr.get("https://mail.163.com/")
        time.sleep(2)
        iframe = self.dr.find_element(by="xpath",
                                      value="/html/body/div[2]/div[3]/div[1]/div/div[4]/div[1]/div[1]/iframe")
        self.dr.switch_to.frame(iframe)  # 切换至内嵌页面
        time.sleep(0.5)
        self.dr.find_element(by="name", value="email").clear()  # 清除内容
        time.sleep(0.5)
        self.dr.find_element(by="name", value="email").send_keys(username)  # 输入账户
        self.dr.find_element(by="name", value="password").clear()  # 清除内容
        time.sleep(0.5)
        self.dr.find_element(by="name", value="password").send_keys(password)
        self.dr.find_element(by="id", value="dologin").click()  # 进入邮箱首页
        self.dr.switch_to.parent_frame()  # 切回父级页面
        time.sleep(2)
        try:
            self.dr.find_element(By.ID, "_mail_component_147_147").click()  # 点击收件箱
        except NoSuchElementException:
            time.sleep(2)
            self.dr.find_element(By.ID, "_mail_component_147_147").click()  # 报错，再次点击一次收件箱

        time.sleep(2)
        count = self.dr.find_elements(By.CLASS_NAME, "nl0.hA0.ck0")
        # print(len(count))  # 获取存在的未读邮件数量
        n = 1
        for i in range(len(count)):
            emailname = self.dr.find_elements(By.CLASS_NAME, "dP0")[i].text  # 遍历未读邮件邮件名
            # print(i)
            # print(emailname)
            # print(name)
            if emailname == name:  # 如果信息名为想匹配的账户名称则执行下一步操作
                if n == no:
                    self.dr.find_elements(By.CLASS_NAME, "dP0")[i].click()  # 点击邮件查看详情
                    time.sleep(1)
                    iframe = self.dr.find_element(By.XPATH,
                                                  "/html/body/div[2]/div[1]/div[3]/div/div[1]/div[6]/div/iframe")  #
                    # 定位内嵌页面
                    self.dr.switch_to.frame(iframe)  # 切换到内嵌页面
                    time.sleep(1)
                    res = self.dr.find_element(By.CLASS_NAME,
                                               'netease_mail_readhtml.netease_mail_readhtml_webmail').text  # 获取整个邮件信息
                    # print(res)
                    self.dr.switch_to.parent_frame()  # 切回父级界面
                    code = re.findall(pattern="\d+", string=res)  # 使用正则表达式获取邮箱验证码
                    # print(code)
                    break  # 获取完成退出遍历
                else:
                    print(f'应为第{no}封符合需求的邮件，此次跳过')
                    n += 1
        self.dr.quit()  # 关闭浏览器
        return code


