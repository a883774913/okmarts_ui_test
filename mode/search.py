"""
搜索模块
"""
import random
import re
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
            print('通道3')
            driver.find_element(by='class name', value='ant-select.ant-select-enabled').click()  # 点击类型
            time.sleep(0.5)
            elements = driver.find_elements(by='class name', value='ant-select-dropdown-menu-item')  # 获取搜索列表中的类型集合
            print(len(elements))        #获取存在的类型数量
            no = random.randint(1, len(elements) - 1)
            driver.find_elements(by='css selector', value='li[class="ant-select-dropdown-menu-item"]')[no].click()  # 点击随机获取的元素
            typeone = driver.find_elements(by='css selector', value='li[class="ant-select-dropdown-menu-item"]')[no].text  # 获取随机获取的文本
            print(f'类型名称为{typeone}')
            search_info = data.split('=', 1)[-1]
            driver.find_element(by='xpath', value='//*[@id="app"]/div/div[1]/div/div[2]/div[2]/span/span/input').send_keys(search_info)  # 输入搜索内容
            driver.find_element(by='xpath', value='//*[@id="app"]/div/div[1]/div/div[2]/div[2]/span/button').click()  # 点击搜索
            time.sleep(2)
            search_goods_infos = driver.find_elements(by='class name', value='title.text-black.margin-bottom-xs ')  # 获取名称集合
            print(search_goods_infos)
            sql = f"SELECT id FROM goods_type WHERE typeone='{typeone}';"
            typeid = Mysql().search_info(user='root', pwd='OKmarts888.,', host='18.118.13.94', db='okmarts', port=3306, sql=sql)  # 获取类型ID
            print(f'类型ID为{typeid[0]["id"]}')
            sql2 = f"select name from (SELECT * FROM goods WHERE typeid='{typeid[0]['id']}') b where name like '%{search_info}%';"
            goodsnames = Mysql().search_info(user='root', pwd='OKmarts888.,', host='18.118.13.94', db='okmarts', port=3306, sql=sql2)  # 获取商品名称集合
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
            print('通道4')
            driver.find_element(by='class name', value='ant-select.ant-select-enabled').click()  # 点击类型
            time.sleep(0.5)
            elements = driver.find_elements(by='class name', value='ant-select-dropdown-menu-item')  # 获取搜索列表中的类型集合
            print(len(elements))  # 获取存在的类型数量
            no = random.randint(1, len(elements) - 1)
            driver.find_elements(by='css selector', value='li[class="ant-select-dropdown-menu-item"]')[no].click()  # 点击随机获取的元素
            typeone = driver.find_elements(by='css selector', value='li[class="ant-select-dropdown-menu-item"]')[no].text  # 获取随机获取的文本
            print(f'类型名称为{typeone}')
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
            infos = driver.find_elements(by='class name', value='title.text-black.margin-bottom-xs ')
            print(f'搜索的结果为{infos}')
            assert infos != []
        elif casename == '连续全文查询五次商品结果是否相同':
            print('通道5')
            n = 1
            while n <= 5:
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
                print(f'第{n - 1}次测试通过')
        elif casename == '点击All Categories 输入商品全称点击回车查询成功':
            print('通道6')
            search_info = data.split('=', 1)[-1]
            print(f'搜索内容为{search_info}')
            driver.find_element(by='xpath', value='//*[@id="app"]/div/div[1]/div/div[2]/div[2]/span/span/input').send_keys(search_info)  # 输入搜索内容
            pk = PyKeyboard()
            pk.press_key(pk.enter_key)  # 按压回车
            pk.release_key(pk.enter_key)  # 释放回车
            time.sleep(4)
            text = driver.find_element(by=f"{assert_way.split('=', 1)[0]}", value=f"{assert_way.split('=', 1)[1]}").text
            print(f'text为{text}')
            assert text == result
        elif casename == '鼠标点击搜索栏，弹出热门搜索，选择相关选项，显示该选项的产品成功':
            print('通道7')
            driver.find_element(by='class name', value='ant-input').click()  # 点击搜索栏
            time.sleep(2)
            driver.find_element(by='class name', value='type-item').click()  # 点击第一个热门搜索
            time.sleep(3)
            self.search_mode1(data, driver)
        elif casename == '搜索栏输入超长字符串搜索失败':
            print('通道8')
            search_info = data.split('=', 1)[-1]
            print(f'搜索内容为{search_info}')
            driver.find_element(by='xpath', value='//*[@id="app"]/div/div[1]/div/div[2]/div[2]/span/span/input').send_keys(search_info)  # 输入搜索内容
            driver.find_element(by='css selector',value='#app > div > div.global-header > div > div.menu-content > div.search-out > span > button').click()
            time.sleep(4)
            text = driver.find_element(by=f"{assert_way.split('=', 1)[0]}", value=f"{assert_way.split('=', 1)[1]}").text
            print(f'text为{text}')
            assert text == result
        elif casename == '搜索出商品后使用High price first排序，显示正确':
            print('通道9')
            self.search_mode2(driver, data, order=0)
        elif casename == '搜索出商品后使用Low price first排序，显示正确':
            print('通道10')
            self.search_mode2(driver, data, order=1)
        elif casename == '搜索出商品后点击相应查询进入商品详情页成功':
            print('通道11')
            search_info = data.split('=', 1)[-1]
            print(f'搜索内容为{search_info}')
            driver.find_element(by='xpath', value='//*[@id="app"]/div/div[1]/div/div[2]/div[2]/span/span/input').send_keys(data.split('=', 1)[-1])  # 输入搜索内容
            driver.find_element(by='xpath', value='//*[@id="app"]/div/div[1]/div/div[2]/div[2]/span/button').click()  # 点击搜索
            time.sleep(3)
            info = driver.find_elements(by='css selector', value='div[class="title text-black margin-bottom-xs "]')[0].text  # 获取第一个商品名称
            print(info)
            assert search_info in info  # 判断搜索内容是否在名称里
            try:
                driver.find_elements(by='css selector', value='div[class="title text-black margin-bottom-xs "] > a ')[0].click()  # 点击商品名称 跳转到详情页面
                time.sleep(2)
                buy_now = driver.find_elements(by='class name', value='atn-btn-orange.ant-btn.ant-btn-block')[1].text  # 判断是否在商品详情页面
                print(f'buy_now为{buy_now}')
                assert buy_now == 'Buy now'
                goods_name = driver.find_element(by='class name', value='title.text-black.margin-bottom-sm').text  # 获取商品详情页面的商品名称
                print(goods_name)
                assert info == goods_name
            except:
                assert False
        elif casename == '通过筛选器Brand筛选到商品成功':
            self.search_mode3(driver,data,mode=int(0))
        elif casename == '通过筛选器Types of筛选到商品成功':
            self.search_mode3(driver, data, mode=int(1))
        elif casename == '通过筛选器Brand和Types of 组合筛选商品成功':
            self.input_search(data, driver)
            brand_text,brand_number = self.mode4(driver,mode=0)       #选择品牌信息，获取品牌数量
            type_text,type_number = self.mode4(driver,mode=1)         #选择类型信息，获取类型数量
            if int(brand_number) == 0 or int(type_number) == 0:   #如果品牌数量或者类型数量其中一个为0
                print('品牌数量或者类型数量其中一个为0,无产品')
                time.sleep(3)
                result = driver.find_element(by='class name', value='tableData-out.nodata.text-black').text
                print(result)
                assert result == 'The keywords you search are not included yet, try other keywords'
            else:
                erro, n, number = self.get_number_n_erro(driver, 2)
                while number >= n:
                    n += 1
                    print(f'第{n}次循环')
                    infos = driver.find_elements(by='class name', value='title.text-black.margin-bottom-xs ')  # 获取商品名称集合
                    print(f'存在{len(infos)}件商品')
                    for info in infos:  # 遍历名称 查询是否有不符合的名称
                        goods_name = info.text  # 获取名称
                        driver.execute_script("arguments[0].scrollIntoView();", info)  # 拖动到可见的元素去
                        print(goods_name)
                        sql1 = f"SELECT brandid,typeid FROM goods where name='{goods_name}';"   #获取品牌ID，类型ID
                        ids = Mysql().search_info(user='root', pwd='OKmarts888.,', host='18.118.13.94', db='okmarts', port=3306, sql=sql1)  # 获取品牌ID、类型ID
                        print(ids)
                        sql2 = f"""SELECT name FROM goods_brand where id="{ids[0]['brandid']}";"""
                        brand_name = Mysql().search_info(user='root', pwd='OKmarts888.,', host='18.118.13.94', db='okmarts', port=3306, sql=sql2)  # 获取品牌名称
                        print(f'brand_name为{brand_name[0]["name"]}')
                        sql3 = f"""SELECT typeone FROM goods_type where id="{ids[0]['typeid']}";"""
                        type_name = Mysql().search_info(user='root', pwd='OKmarts888.,', host='18.118.13.94', db='okmarts', port=3306, sql=sql3)  # 获取品牌名称
                        print(f'type_name为{type_name[0]["typeone"]}')
                        if brand_name[0]["name"] not in brand_text or type_name[0]["typeone"] not in type_text:
                            erro += 1
                        print(erro)
                        assert erro == 0
                    if number == n:
                        print('当前页为循环最后一次')
                        break
                    else:
                        time.sleep(2)
                        driver.find_element(by='class name', value='anticon.anticon-right').click()  # 点击下一页
                        time.sleep(3)
        else:
            print('通道0')
            self.input_search(data, driver)
            self.search_mode1(data, driver)

    def search_mode1(self, data, driver):
        """
        输入搜索内容-点击搜索--断言
        :param data:
        :param driver:
        :return:
        """
        erro, n, number = self.get_number_n_erro(driver, 5)
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

    def search_mode2(self, driver, data, order: int):
        """
        用于搜索页测试排序有无错误使用
        :param driver:  驱动
        :param data: 数据
        :param order: 排序字段，order=0,为降序，order=1 为升序
        :return:
        """
        self.input_search(data, driver)
        driver.find_elements(by='class name', value='ant-select-selection__rendered')[1].click()  # 点击排序
        time.sleep(1)
        driver.find_elements(by='class name', value='ant-select-dropdown-menu-item')[order].click()  # 点击从高往低
        time.sleep(2)
        total_page = self.get_page(driver)  # 获取总页数
        erro, n, number = self.get_number_n_erro(driver, 5)
        while number >= n:
            n += 1
            print(f'第{n}次循环')
            infos = driver.find_elements(by='class name', value='title.text-black.margin-bottom-xs ')  # 获取商品名称集合
            print(f'存在{len(infos)}件商品')
            for i in range(len(infos) - 1):
                print(i)
                driver.execute_script("arguments[0].scrollIntoView();", infos[i])  # 拖动到可见的元素去
                price1 = re.findall('\d+', driver.find_elements(by='class name', value='price.margin-bottom-xs')[i].text)[0]  # 商品价格1
                price2 = re.findall('\d+', driver.find_elements(by='class name', value='price.margin-bottom-xs')[i + 1].text)[0]  # 商品价格2
                print(f'price1为{price1}')
                print(f'price2为{price2}')
                if order == 0:
                    if int(price1) < int(price2):
                        erro += 1
                else:
                    if int(price1) > int(price2):
                        erro += 1
            print(erro)
            assert erro == 0
            if number == n:
                print('当前页为循环最后一次')
                break
            else:
                time.sleep(2)
                driver.find_element(by='class name', value='anticon.anticon-right').click()  # 点击下一页
                time.sleep(3)

    def search_mode3(self,driver,data,mode:int):
        """
        检测筛选功能品牌、类型使用脚本模块
        :param driver: 驱动
        :param data: 数据
        :param n: n=0 为品牌 n= 1为类型
        :return:
        """
        self.input_search(data, driver)
        text,number = self.mode4(driver,mode)
        if number == '0':  # 如果数量为0
            # WebDriverWait(driver,10,0.2).until(lambda x:x.find_element(by='class name', value='tableData-out.nodata.text-black'))
            try:
                time.sleep(3)
                result = driver.find_element(by='class name', value='tableData-out.nodata.text-black').text
                print(result)
                assert result == 'The keywords you search are not included yet, try other keywords'
            except:
                assert False
        else:
            erro, n, number = self.get_number_n_erro(driver, 1)
            while number >= n:
                n += 1
                print(f'第{n}次循环')
                infos = driver.find_elements(by='class name', value='title.text-black.margin-bottom-xs ')  # 获取商品名称集合
                print(f'存在{len(infos)}件商品')
                for info in infos:  # 遍历名称 查询是否有不符合的名称
                    goods_name = info.text  # 获取名称
                    driver.execute_script("arguments[0].scrollIntoView();", info)  # 拖动到可见的元素去
                    print(goods_name)
                    if mode == 0 :
                        print('筛选品牌')
                        sql1 = f"SELECT brandid FROM goods where name='{goods_name}';"
                        id = Mysql().search_info(user='root', pwd='OKmarts888.,', host='18.118.13.94', db='okmarts', port=3306, sql=sql1)  # 获取品牌ID
                        print(f'id为{id}')
                        sql2 = f"""SELECT name FROM goods_brand where id="{id[0]['brandid']}";"""
                        name = Mysql().search_info(user='root', pwd='OKmarts888.,', host='18.118.13.94', db='okmarts', port=3306, sql=sql2)  # 获取品牌名称
                        print(f'name为{name}')

                        print(text)
                        if name[0]['name'] not in text:  # 如果查询出的品牌名称不在勾选的品牌名称内
                            erro += 1
                        assert erro == 0
                    elif mode == 1:
                        print(f'筛选类型')
                        sql1 = f"SELECT typeid FROM goods where name='{goods_name}';"
                        id = Mysql().search_info(user='root', pwd='OKmarts888.,', host='18.118.13.94', db='okmarts', port=3306, sql=sql1)  # 获取品牌ID
                        sql2 = f"""SELECT typeone FROM goods_type where id="{id[0]['typeid']}";"""
                        name = Mysql().search_info(user='root', pwd='OKmarts888.,', host='18.118.13.94', db='okmarts', port=3306, sql=sql2)  # 获取品牌名称
                        if name[0]['typeone'] not in text:  # 如果查询出的品牌名称不在勾选的品牌名称内
                            erro += 1
                        assert erro == 0
                    # print(f'id为{id}')
                    # print(f'name为{name}')
                if number == n:
                    print('当前页为循环最后一次')
                    break
                else:
                    time.sleep(2)
                    driver.find_element(by='class name', value='anticon.anticon-right').click()  # 点击下一页
                    time.sleep(3)

    def mode4(self,driver,mode:int):
        """
        定位到品牌、类型，随机获取一个品牌、类型的文本信息，并勾选该品牌、类型
        :param driver: 驱动
        :param mode: （0，1）0为品牌，1为类型
        :return:text,number     text为品牌、类型相关信息，number为相关信息中的数字，用于判断是否为0
        """
        WebDriverWait(driver,30,0,2).until(lambda x:x.find_elements(by='css selector', value='div[class="ant-checkbox-group"]')[0])
        element = driver.find_elements(by='css selector', value='div[class="ant-checkbox-group"]')[mode]  # 定位到品牌
        elements = element.find_elements(by='class name', value='ant-checkbox-wrapper')  # 寻找该标签下的所有符合要求的元素
        no = random.randint(0, len(elements) - 1)
        text = element.find_elements(by='css selector', value='label[class="ant-checkbox-wrapper')[no].text  # 获取勾选的品牌、类型文本

        element.find_elements(by='css selector', value='input[class="ant-checkbox-input"]')[no].click()  # 勾选相关品牌、类型
        number = re.findall('\d+', text)[0]
        if mode == 1:
            print(f'类型信息为{text}')
            print(f'类型数量为{number}')
        else:
            print(f'品牌信息为{text}')
            print(f'品牌数量为{number}')
        return text,number

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

    def get_number_n_erro(self, driver, num: int):
        """
        设置循环的次数
        :param driver:
        :param num: 循环次数
        :return:
        """
        erro = 0  # 初始化错误个数
        n = 0  # 初始化循环次数
        WebDriverWait(driver, 15, 0.2).until(lambda x: x.find_element(by='class name', value='title.margin-bottom'))
        time.sleep(2)
        total_page = self.get_page(driver)  # 获取总页数
        if total_page > num:
            number = num
        else:
            number = total_page
        return erro, n, number

    def input_search(self, data, driver):
        """
        输入搜索内容，点击搜索
        :param data:
        :param driver:
        :return:
        """
        search_info = data.split('=', 1)[-1]
        print(f'搜索内容为{search_info}')
        driver.find_element(by='xpath', value='//*[@id="app"]/div/div[1]/div/div[2]/div[2]/span/span/input').send_keys(data.split('=', 1)[-1])  # 输入搜索内容
        driver.find_element(by='xpath', value='//*[@id="app"]/div/div[1]/div/div[2]/div[2]/span/button').click()  # 点击搜索
        time.sleep(3)
