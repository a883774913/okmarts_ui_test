"""
导航栏模块
"""
import time


from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from okmarts_ui_test.common.common import Common


class Navigation_Bar:

    def navigation_bar(self,driver,Parameter):
        casename = Parameter['casename']
        mode = Parameter['mode']
        data = Parameter['data'].split('\n')
        print(data)
        assert_way = Parameter['assert_way']
        result = Parameter['result']

        driver.get('http://18.118.13.94:81/index')      #打开首页
        WebDriverWait(driver,30,0.2).until(lambda x:x.find_element(by='class name',value='pointer.all'))
        time.sleep(2)
        if casename == '点击导航栏导航栏伸缩成功':
            if driver.find_element(by='class name',value='okm-icon.icon-leimu').is_displayed(): #如果元素Full catalog 存在
                driver.find_element(by='css selector',value='#app > div > div.global-header > div > div.menu-content '      
                                                            '> div.menu-left > div.menu-out > '
                                                            'div.menu-btn.text-tit-lg > svg').click() #点击导航栏收缩按钮
                time.sleep(2)
                try:
                    print(driver.find_element(by='class name',value='okm-icon.icon-leimu').is_displayed())
                    raise AssertionError
                except NoSuchElementException:
                    assert True
            else:
                print('未找到导航栏')
        elif casename == '点击Full catalog进入所有类别页面':
            driver.find_element(by='class name', value='okm-icon.icon-leimu').click()   #点击full catalog
            WebDriverWait(driver, 30, 0.2).until(lambda x: x.find_element_by_css_selector('#app > div > div.ui-container > div.content.category-content > div.ant-breadcrumb > span:nth-child(1) > span.ant-breadcrumb-separator'))
            text = driver.find_element(by=f"{assert_way.split('=', 1)[0]}",
                                       value=f"{assert_way.split('=', 1)[1]}").text
            print(text)
            print(result)
            assert str(text) == result

        elif casename == '鼠标悬停至导航栏相应类别中，显示该类别所包含的品牌信息成功':
            Common().hover(driver,way='xpath',element='//*[@id="app"]/div/div[1]/div/div[2]/div[1]/div[1]/div[2]/ul/li[1]') #悬停
            time.sleep(2)
            text = driver.find_element(by=f"{assert_way.split('=', 1)[0]}",
                                       value=f"{assert_way.split('=', 1)[1]}").text
            print(text)
            print(result)
            assert str(text) == result

        elif casename == '点击二级分类商品品牌跳转至该品牌页中，且商品成功显示':
            Common().hover(driver,way='xpath',element='//*[@id="app"]/div/div[1]/div/div[2]/div[1]/div[1]/div[2]/ul/li[2]')
            driver.find_element(by='xpath',value='//*[@id="app"]/div/div[1]/div/div[2]/div[1]/div[1]/div[2]/ul/li[2]/div/div[1]/div/div[1]/a').click()
            time.sleep(2)
            text = driver.find_element(by=f"{assert_way.split('=', 1)[0]}",
                                       value=f"{assert_way.split('=', 1)[1]}").text
            print(text)
            print(result)
            assert str(text) == result

        elif casename =='该品牌下无商品，品牌页面正确显示':
            Common().hover(driver,way='xpath',element='//*[@id="app"]/div/div[1]/div/div[2]/div[1]/div[1]/div[2]/ul/li[1]')
            time.sleep(0.5)
            driver.find_element(by='xpath',value='//*[@id="app"]/div/div[1]/div/div[2]/div[1]/div[1]/div[2]/ul/li[1]/div/div[1]/div/div[1]/a').click()
            time.sleep(2)
            text = driver.find_element(by=f"{assert_way.split('=', 1)[0]}",
                                       value=f"{assert_way.split('=', 1)[1]}").text
            print(text)
            print(result)
            assert str(text) == result

        elif casename == 'All Categories 页面可以点击类别快速移动到该类别所在页面位置':
            driver.find_element(by='class name', value='okm-icon.icon-leimu').click()  # 点击full catalog
            time.sleep(2)
            driver.find_element(by='xpath',value='//*[@id="app"]/div[1]/div[2]/div[1]/div[2]/div/div/div/div[2]/div[8]/div/div/a').click()  #点击Water Pump
            time.sleep(1)
            text = driver.find_element(by='xpath',value='//*[@id="type7"]/div[2]/div[44]/a').text
            print(text)
            text = driver.find_element(by=f"{assert_way.split('=', 1)[0]}",
                                       value=f"{assert_way.split('=', 1)[1]}").text
            print(text)
            print(result)
            assert str(text) == result
