"""
帮助中心模块
"""
import time

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait

from okmarts_ui_test.common.common import Common


class Help_Center:

    def help_center(self, driver, Parameter):
        casename = Parameter['casename']
        mode = Parameter['mode']
        data = Parameter['data'].split('\n')
        print(data)
        assert_way = Parameter['assert_way']
        result = Parameter['result']

        driver.get('http://18.118.13.94:81/index')  # 打开首页
        time.sleep(1)
        if '登录状态' in casename:
            Common().is_login(driver,useraccount='979172251@qq.com',password='a123456')
            time.sleep(2)
            if casename == '登录状态点击Retrieve Password页面跳转到修改密码页面':
                print('通道1')
                self.Go(driver, assert_way, result,1)
            elif casename == '登录状态点击Change Email Address(Need to log in first)页面成功跳转至邮箱修改页面':
                self.Go(driver,assert_way,result,2)
            elif casename == '登录状态点击点击Auction payment balance页面正确跳转至拍卖页面':
                self.Go(driver,assert_way,result,3)
            elif casename == '登录状态点击 Order without payment页面正确跳转至购物车页面':
                try:
                    self.Go(driver, assert_way, result, 4)
                except NoSuchElementException:  #如果断言错误 则为存在商品
                    print('购物车存在商品')
                    try:
                        text = driver.find_element(by='css selector',value='#app > div > div > div.ui-container > div.content.flex.space-between > div.auction-info > '
                                                                           'div.title-1.flex.align-center.space-between > div.name.flex.align-center > span').text
                    except NoSuchElementException:
                        time.sleep(1)
                        text = driver.find_element(by='xpath',value='//*[@id="app"]/div/div/div[2]/div[1]/div[1]/div[1]/div[1]/span').text
                    assert text == 'Shopping cart'
            elif casename in ['登录状态意见反馈不输入任何内容发送失败','登录状态意见反馈不输入标题发送失败','登录状态意见反馈不输入内容发送失败','登录状态意见反馈输入正确内容发送成功']:
                print('通道9')
                title = data[0].split('=')[-1]
                descript = data[1].split('=')[-1]
                self.site_message(driver,title=title,descript=descript,assert_way=assert_way,result=result)
        else:   #未登录状态
            Common().Restore_environment(driver)
            if casename == '网站左上角存在帮助中心入口':
                print('通道2')
                text = driver.find_element(by=f"{assert_way.split('=', 1)[0]}",
                                           value=f"{assert_way.split('=', 1)[1]}").is_displayed()
                print(text)
                print(result)
                assert str(text) == result
            elif casename == '点击帮助中心页面成功跳转':
                print('通道3')
                driver.find_element(by='css selector',
                                    value='#app > div > div.global-header > div > div.top-menu > a:nth-child(3)').click()  # 点击帮助中心
                WebDriverWait(driver, 30, 0.2).until(lambda x: x.find_element_by_css_selector(
                    "#app > div > div.ui-container > div.content.page-help-content > div:nth-child(1) > div.text-tit-lg"))
                text = driver.find_element(by=f"{assert_way.split('=', 1)[0]}",
                                           value=f"{assert_way.split('=', 1)[1]}").text
                print(text)
                assert text == result
            elif casename == '未登录状态点击Retrieve Password页面跳转到登录页面':
                print('通道4')
                self.Go(driver, assert_way, result,1)
            elif casename == '点击Change Email Address(Need to log in first)页面成功跳转至登录页面':
                print('通道5')
                self.Go(driver,assert_way,result,2)
            elif casename == '点击Auction payment balance页面正确跳转至登录页面':
                print('通道6')
                self.Go(driver,assert_way,result,3)
            elif casename == '点击 Order without payment页面正确跳转至登录页面':
                print('通道7')
                self.Go(driver,assert_way,result,4)
            elif casename == '存在意见反馈模块':
                print('通道8')
                driver.find_element(by='css selector',
                                    value='#app > div > div.global-header > div > div.top-menu > a:nth-child(3)').click()  # 点击帮助中心
                WebDriverWait(driver, 30, 0.2).until(lambda x: x.find_element_by_css_selector(
                    "#app > div > div.ui-container > div.content.page-help-content > div:nth-child(1) > div.text-tit-lg"))
                Common().huadong(driver,by='css selector',value='#app > div.page-myCenter.page-help.transparent-header.transparent > div.ui-container > div.content.page-help-content > div.site-message.clearfix > div.text-tit-lg.margin-bottom-xs')
                text = driver.find_element(by=f"{assert_way.split('=', 1)[0]}",
                                           value=f"{assert_way.split('=', 1)[1]}").text
                print(text)
                assert text == result

    # 点击帮助中心-点击修改密码-断言
    def Go(self, driver, assert_way, result,number):
        """
        进入第几个入口
        :param driver:
        :param assert_way:
        :param result:
        :param number: 1为Retrieve Password 2为Change Email Address(Need to log in first)
        :return:
        """
        driver.find_element(by='css selector',
                            value='#app > div > div.global-header > div > div.top-menu > a:nth-child(3)').click()  # 点击帮助中心
        WebDriverWait(driver, 30, 0.2).until(lambda x: x.find_element_by_css_selector(
            "#app > div > div.ui-container > div.content.page-help-content > div:nth-child(1) > div.text-tit-lg"))
        driver.find_element(by='css selector',
                            value=f'#app > div > div.ui-container > div.content.page-help-content > div:nth-child(1) > div.flex.href-list.space-between.text-xs > '
                                  f'a:nth-child({number})').click()
        time.sleep(3)
        text = driver.find_element(by=f"{assert_way.split('=', 1)[0]}",
                                   value=f"{assert_way.split('=', 1)[1]}").text
        print(f'text为{text}')
        assert text == result

    #意见反馈模块
    def site_message(self,driver,title,descript,assert_way,result):
        """
        意见反馈模块输入信息断言
        :param driver: 驱动
        :param title: 标题
        :param descript: 描述
        :param assert_way: 断言方式
        :param result:断言结果
        :return:
        """
        driver.find_element(by='css selector',
                            value='#app > div > div.global-header > div > div.top-menu > a:nth-child(3)').click()  # 点击帮助中心
        WebDriverWait(driver, 30, 0.2).until(lambda x: x.find_element_by_css_selector(
            "#app > div > div.ui-container > div.content.page-help-content > div:nth-child(1) > div.text-tit-lg"))  #等待打开
        Common().huadong(driver, by='css selector',
                         value='#app > div.page-myCenter.page-help.transparent-header.transparent > div.ui-container '
                               '> div.content.page-help-content > div.site-message.clearfix > '
                               'div.text-tit-lg.margin-bottom-xs')      #滑动到指定位置
        driver.find_element(by='css selector',value='#app > div.page-myCenter.page-help.transparent-header'
                                                    '.transparent > div.ui-container > div.content.page-help-content '
                                                    '> div.site-message.clearfix > input').click()
        driver.find_element(by='css selector',value='#app > div.page-myCenter.page-help.transparent-header'
                                                    '.transparent > div.ui-container > div.content.page-help-content '
                                                    '> div.site-message.clearfix > input').send_keys(title)       #输入标题
        driver.find_element(by='xpath',value='//*[@id="app"]/div[1]/div[2]/div[1]/div[4]/textarea').click()
        driver.find_element(by='xpath',value='//*[@id="app"]/div[1]/div[2]/div[1]/div[4]/textarea').send_keys(descript) #输入描述正文
        time.sleep(2)
        driver.find_element(by='xpath',value='/html/body/div[1]/div[1]/div[2]/div[1]/div[4]/button').click()            #点击发送
        time.sleep(1.4)
        text = driver.find_element(by=f"{assert_way.split('=', 1)[0]}",
                                   value=f"{assert_way.split('=', 1)[1]}").text
        print(f'text 为 {text}')
        print(f'result 为 {result}')
        assert text == result