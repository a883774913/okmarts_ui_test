"""
搜索模块
"""
import random
import time

from pykeyboard.windows import PyKeyboard
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait

from okmarts_ui_test.common.common import Common
from okmarts_ui_test.mysql.mysql import Mysql


class Search:

    def search(self, driver, Parameter):
        casename = Parameter['casename']
        data = Parameter['data']
        assert_way = Parameter['assert_way']
        result = Parameter['result']
        driver.get('http://18.118.13.94:81/index')  # 打开首页
        WebDriverWait(driver, 20, 0.2).until(lambda x: x.find_element(by='xpath', value='//*[@id="app"]/div/div[1]/div/div[2]/div[3]/div[3]/span[1]'))
        time.sleep(2)
        if casename == '首页存在搜索栏':
            print('通道1')
            text = driver.find_element(by=f"{assert_way.split('=', 1)[0]}", value=f"{assert_way.split('=', 1)[1]}").is_displayed()
            print(text)
            assert text is bool(result)
        elif casename == '不输入任何内容点击查询弹出错误提示':
            print('通道2')
            driver.find_element(by='xpath', value='//*[@id="app"]/div/div[1]/div/div[2]/div[2]/span/button').click()  # 点击搜索
            time.sleep(2)
            text = driver.find_element(by=f"{assert_way.split('=', 1)[0]}", value=f"{assert_way.split('=', 1)[1]}").text
            print(f'text为{text}')
            assert text == result
        elif casename == '随机选择一个类型模糊搜索成功':
            driver.find_element(by='class name',value='ant-select.ant-select-enabled').click()  #点击类型
            time.sleep(0.5)
            elements = driver.find_elements(by='class name',value='ant-select-dropdown-menu-item')      #获取搜索列表中的类型集合
            random_element = random.choice(elements)        #随机选择一个类别
            random_element.click()      #点击随机获取的元素
            typeone = random_element.text  #获取随机获取的文本
            print(typeone)
            search_info = data.split('=', 1)[-1]
            driver.find_element(by='xpath', value='//*[@id="app"]/div/div[1]/div/div[2]/div[2]/span/span/input').send_keys(search_info)  # 输入搜索内容
            driver.find_element(by='xpath', value='//*[@id="app"]/div/div[1]/div/div[2]/div[2]/span/button').click()  # 点击搜索
            time.sleep(2)
            search_goods_infos = driver.find_elements(by='class name',value='title.text-black.margin-bottom-xs ')       #获取名称集合
            print(search_goods_infos)
            sql = f"SELECT id FROM goods_type WHERE typeone='{typeone}';"
            typeid = Mysql().search_info(user='root',pwd='OKmarts888.,',host='18.118.13.94',db='okmarts',port=3306,sql=sql)     #获取类型ID
            print(typeid[0]['id'])
            sql2 = f"select name from (SELECT * FROM goods WHERE typeid='{typeid[0]['id']}') b where name like '%{search_info}%';"
            goodsnames =Mysql().search_info(user='root',pwd='OKmarts888.,',host='18.118.13.94',db='okmarts',port=3306,sql=sql2)     #获取商品名称集合
            print(goodsnames)
            print(len(goodsnames))
            if not search_goods_infos:
                print('未搜索出商品数据')
                assert len(goodsnames) == 0
            else:
                name_list = []
                for info in goodsnames:
                    print(info['name'])
                    name_list.append(info['name'])
                assert random.choice(search_goods_infos).text in name_list
        elif casename == '随机选择一个类型全文搜索成功':
            driver.find_element(by='class name', value='ant-select.ant-select-enabled').click()  # 点击类型
            time.sleep(0.5)
            elements = driver.find_elements(by='class name', value='ant-select-dropdown-menu-item')  # 获取搜索列表中的类型集合
            random_element = random.choice(elements)  # 随机选择一个类别
            random_element.click()  # 点击随机获取的元素
            typeone = random_element.text  # 获取随机获取的文本
            print(typeone)
            sql = f"SELECT id FROM goods_type WHERE typeone='{typeone}';"
            typeid = Mysql().search_info(user='root', pwd='OKmarts888.,', host='18.118.13.94', db='okmarts', port=3306, sql=sql)  # 获取类型ID
            print(typeid[0]['id'])
            sql2 = f"SELECT name FROM goods where typeid='{typeid[0]['id']}';"
            goodsnames = Mysql().search_info(user='root', pwd='OKmarts888.,', host='18.118.13.94', db='okmarts', port=3306, sql=sql2)  # 获取商品名称集合
            print(goodsnames)
            search_info = random.choice(goodsnames)['name']
            print(f'输入的内容为{search_info}')
            driver.find_element(by='xpath', value='//*[@id="app"]/div/div[1]/div/div[2]/div[2]/span/span/input').send_keys(search_info)  # 输入搜索内容
            driver.find_element(by='xpath', value='//*[@id="app"]/div/div[1]/div/div[2]/div[2]/span/button').click()  # 点击搜索
            time.sleep(2)
            infos = driver.find_elements(by='class name',value='title.text-black.margin-bottom-xs ')
            print(f'搜索的结果为{infos}')
            assert infos != []
        elif casename == '连续全文查询五次商品结果是否相同':
            n = 1
            while n <= 5 :
                n += 1
                driver.get('http://18.118.13.94:81/index')  # 打开首页
                WebDriverWait(driver, 20, 0.2).until(lambda x: x.find_element(by='xpath', value='//*[@id="app"]/div/div[1]/div/div[2]/div[3]/div[3]/span[1]'))
                time.sleep(2)
                search_info = data.split('=', 1)[-1]
                print(f'搜索内容为{search_info}')
                driver.find_element(by='xpath', value='//*[@id="app"]/div/div[1]/div/div[2]/div[2]/span/span/input').send_keys(search_info)  # 输入搜索内容
                driver.find_element(by='xpath', value='//*[@id="app"]/div/div[1]/div/div[2]/div[2]/span/button').click()  # 点击搜索
                WebDriverWait(driver, 15, 0.2).until(lambda x: x.find_element(by='class name', value='title.margin-bottom'))
                time.sleep(3)
                text = driver.find_element(by=f"{assert_way.split('=', 1)[0]}", value=f"{assert_way.split('=', 1)[1]}").text
                print(f'text为{text}')
                assert text == result
                print(f'第{n-1}次测试通过')
        elif casename == '点击All Categories 输入商品全称点击回车查询成功':
            search_info = data.split('=', 1)[-1]
            print(f'搜索内容为{search_info}')
            driver.find_element(by='xpath', value='//*[@id="app"]/div/div[1]/div/div[2]/div[2]/span/span/input').send_keys(search_info)  # 输入搜索内容
            pk = PyKeyboard()
            pk.press_key(pk.enter_key)      #按压回车
            pk.release_key(pk.enter_key)    #释放回车
            WebDriverWait(driver, 15, 0.2).until(lambda x: x.find_element(by='class name', value='title.margin-bottom'))
            time.sleep(3)
            text = driver.find_element(by=f"{assert_way.split('=', 1)[0]}", value=f"{assert_way.split('=', 1)[1]}").text
            print(f'text为{text}')
            assert text == result
        elif casename == '鼠标点击搜索栏，弹出热门搜索，选择相关选项，显示该选项的产品成功':
            driver.find_element(by='class name',value='ant-input').click()      #点击搜索栏
            time.sleep(2)
            driver.find_element(by='class name',value='type-item').click()      #点击第一个热门搜索
            time.sleep(3)
            self.search_mode1(data,driver)
        elif casename == '搜索栏输入超长字符串搜索失败':
            search_info = data.split('=', 1)[-1]
            print(f'搜索内容为{search_info}')
            driver.find_element(by='xpath', value='//*[@id="app"]/div/div[1]/div/div[2]/div[2]/span/span/input').send_keys(search_info)  # 输入搜索内容
            pk = PyKeyboard()
            pk.press_key(pk.enter_key)  # 按压回车
            pk.release_key(pk.enter_key)  # 释放回车
            WebDriverWait(driver, 15, 0.2).until(lambda x: x.find_element(by='class name', value='title.margin-bottom'))
            time.sleep(3)
            text = driver.find_element(by=f"{assert_way.split('=', 1)[0]}", value=f"{assert_way.split('=', 1)[1]}").text
            print(f'text为{text}')
            assert text == result
        else:
            print('通道0')
            search_info = data.split('=', 1)[-1]
            print(f'搜索内容为{search_info}')
            driver.find_element(by='xpath', value='//*[@id="app"]/div/div[1]/div/div[2]/div[2]/span/span/input').send_keys(data.split('=', 1)[-1])  # 输入搜索内容
            driver.find_element(by='xpath', value='//*[@id="app"]/div/div[1]/div/div[2]/div[2]/span/button').click()  # 点击搜索
            self.search_mode1(data,driver)

    def search_mode1(self,data,driver):
        """
        输入搜索内容-点击搜索--断言
        :param data:
        :param driver:
        :return:
        """
        erro = 0  # 初始化错误个数
        n = 0  # 初始化循环次数
        WebDriverWait(driver, 15, 0.2).until(lambda x: x.find_element(by='class name', value='title.margin-bottom'))
        time.sleep(2)
        total_page = self.get_page(driver)  # 获取总页数
        if total_page > 5:
            number = 5
        else:
            number = total_page
        while number >= n:
            n += 1
            print(f'第{n}次循环')
            infos = driver.find_elements(by='class name', value='title.text-black.margin-bottom-xs ')  # 获取商品名称集合
            print(f'存在{len(infos)}件商品')
            for info in infos:  # 遍历名称 查询是否有不符合的名称
                print(info.text)
                driver.execute_script("arguments[0].scrollIntoView();", info)  # 拖动到可见的元素去
                if data.split('=', 1)[-1] not in info.text:
                    erro += 1
            assert erro == 0
            if number == n:
                print('当前页为循环最后一次')
                break
            else:
                time.sleep(2)
                driver.find_element(by='class name', value='anticon.anticon-right').click()  # 点击下一页
                time.sleep(3)

    def get_page(self, driver):
        """
        获取搜索出来的商品页数
        :param driver:
        :return:
        """
        try:
            Common().huadong(driver, by='class name', value='pagination-out.text-center')
            time.sleep(2)
            try:
                total_page = int(driver.find_element(by='css selector', value='ul[class="ant-pagination"] > li:nth-last-child(2)').get_attribute('title'))
            except NoSuchElementException:
                print('只有一页')
                total_page = 1
            print(f'总页数为{total_page}')
            return total_page
        except NoSuchElementException:
            info = driver.find_element(by='class name', value='tableData-out.nodata.text-black').text
            print(info)
            if info == 'The keywords you search are not included yet, try other keywords':
                print('未找到商品')
                raise NoSuchElementException
