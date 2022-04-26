"""
导航栏模块
"""
import time


class Navigation_Bar:

    def navigation_bar(self,driver,Parameter):
        casename = Parameter['casename']
        mode = Parameter['mode']
        data = Parameter['data'].split('\n')
        print(data)
        assert_way = Parameter['assert_way']
        result = Parameter['result']

        driver.get('http://18.118.13.94:81/index')      #打开首页
        time.sleep(1)
        if casename == '点击导航栏导航栏伸缩成功':
            if driver.find_element(by='class name',value='okm-icon.icon-leimu').is_displayed(): #如果元素Full catalog 存在
                driver.find_element(by='css selector',value='#app > div > div.global-header > div > div.menu-content '      
                                                            '> div.menu-left > div.menu-out > '
                                                            'div.menu-btn.text-tit-lg > svg').click() #点击导航栏收缩按钮
                time.sleep(1)
                print(driver.find_element(by='class name',value='okm-icon.icon-leimu').is_displayed())
                assert driver.find_element(by='class name',value='okm-icon.icon-leimu').is_displayed() == 'False'
            else:
                print('未找到导航栏')
        elif casename == '点击Full catalog进入所有类别页面':
            driver.find_element(by='class name', value='okm-icon.icon-leimu').click()

