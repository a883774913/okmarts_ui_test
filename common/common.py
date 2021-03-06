import json
import os
import random
import time

import requests
import xlrd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.support.wait import WebDriverWait

from okmarts_ui_test.mode.get_code import Get_Code
from okmarts_ui_test.mysql.mysql import Mysql


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
        cmd1 = 'TASKKILL /F /IM chrome.exe /T'
        cmd2 = 'TASKKILL /F /IM chromedriver.exe /T'
        # cmd1 = 'TASKKILL /F /IM msedge.exe /T'
        # cmd2 = 'TASKKILL /F /IM msedgewebview2.exe /T'
        os.system(cmd1)
        os.system(cmd2)


    def login(self,driver,useraccount,password):
        """
        登录页面进行登录，输入账户密码点击登录
        :param driver: 驱动
        :param useraccount: 账户
        :param password: 密码
        :return:
        """
        print(f'登录账户为{useraccount}')
        driver.find_element(by='id', value='horizontal_login_userAccount').send_keys(useraccount)  # 登录
        driver.find_element(by='id', value='horizontal_login_password').send_keys(password)
        driver.find_element(by='class name', value='atn-btn-orange.ant-btn.ant-btn-lg.ant-btn-block').click()
        time.sleep(1.5)
        try:
            info = driver.find_element(by='xpath',value='/html/body/div[2]/span/div/div/div/span').text
            print(f'登录提示信息为{info}')
        except NoSuchElementException:
            time.sleep(0.3)
            info = driver.find_element(by='xpath', value='/html/body/div[2]/span/div/div/div/span').text
            print(f'登录提示信息为{info}')
        time.sleep(2)

    def Restore_environment(self, dr):
        """
        检测是否为登录状态，如果登录退出登录状态，如果未登录则PASS
        :param dr:  驱动
        :return:
        """
        dr.get('http://18.118.13.94:81/index')
        if dr.find_element(by='xpath',
                           value='//*[@id="app"]/div/div[1]/div/div[2]/div[3]/div[1]').text == 'Login':  # 如果为login 则为未登录状态
            print('未登录，不执行任何操作')
            pass
        else:
            print('登录状态，执行退出登录')
            dr.find_element(by='xpath',
                            value='//*[@id="app"]/div/div[1]/div/div[2]/div[3]/div[1]').click()  # 点击按钮进入个人中心
            time.sleep(1.5)
            dr.find_element(by='class name', value='login-out.text-white').click()  # 点击注销
            time.sleep(1)
            dr.find_element(by='class name', value='ant-btn.ant-btn-primary.ant-btn-sm').click()  # 点击确认
            time.sleep(2)
            print('退出登录完成...')

    def is_login(self,driver,useraccount,password):
        """
        首页检测是否为登录状态，如果登录则PASS，如果未登录则进行登录
        :param driver: 驱动
        :param useraccount: 用户名
        :param password ： 密码
        :return:
        """
        is_login = driver.find_element(by='css selector',
                                       value='#app > div > div.global-header > div > div.menu-content > div.menu-right.flex > div:nth-child(1) > span').text
        if is_login == 'Login':  # 为未登录状态
            print('未登录，正在执行登录')
            driver.find_element(by='css selector',
                                value='#app > div > div.global-header > div > div.menu-content > div.menu-right.flex > div:nth-child(1) > span').click()  # 点击登录
            WebDriverWait(driver, 30, 0.2).until(lambda x: x.find_element_by_class_name(
                "title.text-tit-lg.margin-bottom-lg"))
            Common().login(driver, useraccount=useraccount, password=password)
        else:
            print('已登录')
            pass

    #滑动到页面指定位置
    def huadong(self,driver,by,value):
        """
        滑动页面至指定位置
        :param driver:  驱动
        :param by:  定位方式
        :param value: 定位元素
        :return:
        """
        target = driver.find_element(by=f'{by}',value=f'{value}')
        driver.execute_script("arguments[0].scrollIntoView();", target)  # 拖动到可见的元素去

    #悬停方法
    def hover(self,driver,way,element):
        """
        悬停操作
        :param driver:驱动
        :param way: 定位方法
        :param element: 元素位置
        :return:
        """
        # 定位到要悬停的元素
        above = driver.find_element(by=f'{way}',value=f'{element}')
        # 对定位的元素执行鼠标悬停操作,perform为提交所有ActionChains类中存储的行为
        ActionChains(driver).move_to_element(above).perform()


    def first_name(self):
        first_name = ['赵', '钱', '孙', '李', '周', '吴', '郑', '王', '冯', '陈', '褚', '卫', '蒋', '沈', '韩', '杨', '朱', '秦', '尤',
                      '许', '何', '吕', '施', '张',
                      '孔', '曹', '严', '华', '金', '魏', '陶', '姜', '戚', '谢', '邹', '喻', '柏', '水', '窦', '章', '云', '苏', '潘',
                      '葛', '奚', '范', '彭', '郎',
                      '鲁', '韦', '昌', '马', '苗', '凤', '花', '方', '俞', '任', '袁', '柳', '酆', '鲍', '史', '唐', '费', '廉', '岑',
                      '薛', '雷', '贺', '倪', '汤',
                      '滕', '殷', '罗', '毕', '郝', '邬', '安', '常', '乐', '于', '时', '傅', '皮', '卞', '齐', '康', '伍', '余', '元',
                      '卜', '顾', '孟', '平', '黄',
                      '和', '穆', '萧', '尹', '姚', '邵', '湛', '汪', '祁', '毛', '禹', '狄', '米', '贝', '明', '臧', '计', '伏', '成',
                      '戴', '谈', '宋', '茅', '庞',
                      '熊', '纪', '舒', '屈', '项', '祝', '董', '梁', '杜', '阮', '蓝', '闵', '席', '季', '麻', '强', '贾', '路', '娄',
                      '危', '江', '童', '颜', '郭',
                      '梅', '盛', '林', '刁', '钟', '丘', '徐', '邱', '骆', '高', '夏', '蔡', '田', '樊', '胡', '凌', '霍', '虞', '万',
                      '支', '柯', '昝', '管', '卢',
                      '莫', '经', '房', '裘', '缪', '干', '解', '应', '宗', '丁', '宣', '贲', '邓', '单', '杭', '洪', '包', '诸', '左',
                      '石', '崔', '吉', '钮', '龚',
                      '程', '嵇', '邢', '滑', '裴', '陆', '荣', '翁', '荀', '羊', '於', '惠', '甄', '曲', '家', '封', '芮', '羿', '储',
                      '靳', '汲', '邴', '糜', '松',
                      '井', '段', '富', '巫', '乌', '焦', '巴', '弓', '牧', '隗', '山', '谷', '车', '侯', '宓', '蓬', '全', '郗', '班',
                      '仰', '秋', '仲', '伊', '宫',
                      '宁', '仇', '栾', '暴', '甘', '钭', '厉', '戎', '祖', '武', '符', '刘', '景', '詹', '束', '龙', '叶', '幸', '司',
                      '韶', '郜', '黎', '蓟', '薄',
                      '印', '宿', '白', '怀', '蒲', '台', '从', '鄂', '索', '咸', '籍', '赖', '卓', '蔺', '屠', '蒙', '池', '乔', '阴',
                      '郁', '胥', '能', '苍', '双',
                      '闻', '莘', '党', '翟', '谭', '贡', '劳', '逢', '逄', '姬', '申', '扶', '堵', '冉', '宰', '郦', '雍', '璩', '桑',
                      '桂', '濮', '牛', '寿', '通',
                      '边', '扈', '燕', '冀', '郏', '浦', '尚', '农', '温', '别', '庄', '晏', '柴', '瞿', '阎', '充', '慕', '连', '茹',
                      '习', '宦', '艾', '鱼', '容',
                      '向', '古', '易', '慎', '戈', '廖', '庚', '终', '暨', '居', '衡', '步', '都', '耿', '满', '弘', '匡', '国', '文',
                      '寇', '广', '禄', '阙', '东',
                      '欧', '殳', '沃', '利', '蔚', '越', '夔', '隆', '师', '巩', '厍', '聂', '晁', '勾', '敖', '融', '冷', '訾', '辛',
                      '阚', '那', '简', '饶', '空',
                      '曾', '毋', '沙', '乜', '养', '鞠', '须', '丰', '巢', '关', '蒯', '相', '查', '荆', '红', '游', '竺', '权', '逯',
                      '盖', '益', '桓', '公', '晋',
                      '楚', '阎', '法', '汝', '鄢', '涂', '钦', '归', '海', '岳', '帅', '缑', '亢', '况', '后', '有', '琴', '商', '牟',
                      '佘', '佴', '伯', '赏', '墨',
                      '哈', '谯', '笪', '年', '爱', '阳', '佟', '言', '福']
        random_firstname = random.choice(first_name)
        return random_firstname

    def last_name(self):
        second_name = ['瑾', '雨', '钰', '静', '云', '珺', '惠', '惠', '晴', '岚', '云', '晴', '怡', '裕', '涵', '惠', '涵', '雯', '寒',
                       '润', '秉', '晴', '淑', '珺', '云', '舒', '素', '花', '岚', '清', '寒', '涵', '岚', '欣', '熙', '岚', '寒', '茹',
                       '寒', '岚', '正', '琳', '淑', '惠', '寒', '涵', '晴', '妍', '榕', '寒', '云', '茵', '茵', '惠', '洁', '雨', '翔',
                       '淑', '晴', '珺', '清', '梓', '雯', '雯', '雯', '茜', '云', '清', '秀', '欣', '惠', '茜', '茜', '舒', '婷', '晓',
                       '芷', '欣', '曦', '婷', '莉', '东', '巧', '佳', '秀', '新', '依', '欣', '梦', '菁', '泽', '怡', '陈', '婧', '美',
                       '悦', '莹', '莉', '德', '燕', '瑛', '鹤', '蓉', '佳', '蔡', '婧', '斯', '恺', '珂', '小', '成', '倩', '优', '长',
                       '瑜', '姝', '春', '华', '妍', '娉', '燕', '妍', '静', '禾', '妍', '惋', '清', '茜', '涵', '惠', '茵', '岚', '茜',
                       '媛', '珺', '茹', '涵', '翔', '雨', '思', '寒', '茜', '茜', '涵', '淑', '辰', '贞', '舒', '清', '茵', '淑', '媛',
                       '琳', '君', '云', '寒', '云', '岚', '淑', '颜', '真', '雯', '晴', '雯', '雯', '清', '青', '妍', '芬', '恬', '芙',
                       '宸', '翾', '丽', '悦', '桐', '铭', '睿', '莉', '长', '丽', '夕', '琳', '燕', '善', '琴', '筱', '旭', '蝾', '怡',
                       '莉', '芹', '翔', '晴', '晴', '雅', '茹', '若', '娅', '翔', '惠', '云', '茹', '雯', '寒', '舒', '雅', '雯', '岚',
                       '雯', '茜', '寒', '涵', '晴', '茜', '云', '岚', '茵', '莉', '梦', '涵', '茵', '晴', '岚', '涵', '雯', '惠', '寒',
                       '淑', '岚', '婷', '梓', '秀', '瑶', '芝', '娅', '树', '小', '厦', '卷', '欣', '世', '艳', '丹', '玲', '卓', '杭',
                       '玲', '睿', '炜', '雨', '炜', '丽', '忠', '瑞', '婧', '惠', '炎', '秀', '翠', '爱', '艳', '龙', '嫣', '志', '芷',
                       '悦', '红', '焱', '婷', '惠', '于', '沁', '诺', '梓', '秀', '昊', '小', '悦', '秀', '欣', '晓', '午', '会', '龙',
                       '琳', '展', '羽', '艺', '月', '歌', '海', '晶', '尤', '仪', '玉', '钰', '雪', '卿', '晓', '家', '安', '湘', '丹',
                       '薏', '婷', '怡', '琳', '卓', '瓶', '爱', '桂', '石', '腊', '雅', '莉', '娟', '艳', '棠', '悦', '婉', '嘉', '彩',
                       '媛', '美', '莉', '燕', '昕', '倡', '紊', '子', '爱', '维', '思', '振', '鸾', '玲', '旦', '苏', '羽', '秋', '建',
                       '泓', '富', '倩', '诗', '承', '雪', '妍', '晓', '依', '瑾', '永', '翰', '婉', '景', '赛', '晓', '晋', '幸', '歆',
                       '曾', '国', '彩', '三', '雪', '义', '雪', '津', '琳', '燕', '纯', '素', '艳']
        three = ['萱', '嘉', '彤', '香', '舒', '睿', '雅', '睿', '茜', '嫦', '涵', '惠', '翎', '梅', '惠', '絮', '菡', '婷', '淑', '洁',
                 '文', '清', '涵', '涵', '华', '媛', '娅', '曼', '雅', '华', '菊', '茵', '菡', '琳', '玉', '菲', '云', '絮', '媛', '瑜',
                 '妍', '竣', '淑', '语', '华', '婷', '珺', '如', '嫣', '瑜', '嫦', '清', '嫣', '云', '玲', '蓉', '雯', '梦', '菡', '云',
                 '雅', '婧', '婧', '嘉', '舒', '菡', '嫣', '梦', '珊', '怡', '茜', '华', '茜', '菲', '雯', '悦', '秀', '瑶', '秀', '丽',
                 '娜', '玲', '娜', '艳', '秀', '颖', '娜', '瑶', '洁', '茹', '芳', '若', '红', '宁', '怡', '帆', '莹', '绫', '梅', '萍',
                 '蔓', '梅', '华', '莉', '琳', '妍', '玉', '玲', '妍', '莉', '美', '冰', '美', '丽', '文', '瑶', '颖', '琳', '婷', '娟',
                 '艳', '青', '美', '悦', '凌', '洁', '嘉', '媛', '茹', '晴', '惠', '雁', '菲', '菲', '绮', '菲', '嫣', '鸣', '花', '艳',
                 '岚', '嫦', '菊', '媛', '云', '蓉', '颖', '嫣', '云', '萍', '华', '语', '爰', '茹', '晴', '鸣', '清', '华', '惠', '英',
                 '文', '语', '茹', '晴', '睿', '茜', '蓉', '羽', '迎', '梨', '婕', '旋', '琳', '霞', '淇', '卿', '倩', '琳', '娉', '英',
                 '美', '文', '涵', '星', '玲', '子', '雪', '妍', '婷', '婷', '颖', '悦', '嘉', '岚', '翠', '舒', '语', '美', '清', '媛',
                 '嘉', '絮', '云', '翔', '睿', '玉', '淑', '嫣', '茹', '淑', '云', '嫣', '绮', '睿', '梦', '菡', '萍', '雅', '萍', '丽',
                 '菲', '茹', '茵', '婷', '语', '瑛', '淑', '雁', '雅', '舒', '雯', '悦', '娟', '华', '蓉', '庭', '艳', '霞', '洁', '玉',
                 '颖', '悦', '蓉', '洁', '娇', '妍', '英', '丽', '颖', '琳', '莹', '婷', '英', '燕', '芬', '文', '芳', '琳', '颖', '萍',
                 '茹', '霞', '艳', '钰', '芳', '茹', '颖', '英', '霞', '秀', '玲', '娜', '媛', '瑶', '燕', '君', '怡', '妍', '张', '芳',
                 '怡', '梅', '瑶', '霞', '梅', '敏', '文', '莹', '萍', '玲', '玲', '燕', '婧', '文', '琳', '娟', '洁', '娟', '蓉', '洁',
                 '颖', '茹', '媛', '梅', '冉', '昱', '可', '淼', '婷', '花', '萍', '燕', '英', '梅', '莉', '娅', '娣', '红', '莉', '驰',
                 '婷', '洁', '红', '雪', '芳', '轩', '齐', '妍', '文', '文', '婧', '琴', '娟', '娜', '文', '瑶', '丽', '娅', '娟', '洁',
                 '艳', '颖', '茹', '霞', '成', '茹', '文', '芬', '玲', '霞', '婷', '琳', '琴', '颖', '燕', '文', '玉', '玉', '玉', '瑶',
                 '琳', '燕', '政', '娟', '婷', '婧', '文', '萍', '文', '秀', '明', '洁', '莉', '玲']
        li = [random.choice(second_name), random.choice(three)]
        random_lastname = random.choice(li)
        return random_lastname

    def change_password(self,driver,useraccount,password,code):
        """
        通过忘记密码版块还原密码
        :param code: 上次执行的验证码，用于快速还原
        :param driver: 驱动
        :param useraccount: 账户名
        :param password: 需要修改的密码
        :return:
        """
        print('还原密码环境中'.center(60, '-'))
        driver.maximize_window()
        driver.get('http://18.118.13.94:81/index')
        WebDriverWait(driver, 20, 0.2).until(lambda x: x.find_element(by='xpath', value='//*[@id="app"]/div/div[1]/div/div[2]/div[3]/div[3]/span[1]'))
        driver.find_element(by='class name',value='r_text').click() #点击头像
        time.sleep(1)
        driver.find_element(by='class name',value='login-form-forgot').click()  #点击忘记密码
        time.sleep(1)
        driver.find_element(by='id', value='horizontal_login_userName').send_keys(useraccount)  # 输入用户名
        driver.find_element(by='id', value='horizontal_login_newPassword').send_keys(password)  # 输入新密码
        driver.find_element(by='xpath', value='//*[@id="app"]/div/div[1]/div[2]/form/div[2]/div/div/span/div/div[2]/a').click()  # 点击发送邮件
        time.sleep(1)
        while True:
            info = driver.find_element(by='xpath',value='/html/body/div[2]/span/div/div/div/span').text     #获取发送邮件后的文本
            time.sleep(3)
            print(f'点击发送邮件后提示为{info}')
            if info == 'No such user information！':
                print('账户不存在，请检查账户是否正确！！')
                break
            elif info == 'Please go to your email to check the verification code and enter it': #发送成功
                time.sleep(9)
                code = Get_Code().wangyi(username=useraccount,password='Qwe3541118',name='hydraulic',no=1)
                driver.find_element(by='id', value='horizontal_login_code').send_keys(Keys.CONTROL, 'a')  # 输入验证码
                driver.find_element(by='id',value='horizontal_login_code').send_keys(code)          #输入验证码
                driver.find_element(by='class name',value='atn-btn-orange.ant-btn.ant-btn-lg.ant-btn-block').click()        #点击提交
                WebDriverWait(driver,10,0.2).until(lambda x:x.find_element(by='xpath',value='/html/body/div[2]/span/div/div/div/span'))
                result = driver.find_element(by='xpath',value='/html/body/div[2]/span/div/div/div/span').text        #获取提交后的文本提示
                time.sleep(3)
                print(result)
                if result == 'Verification code error':     #验证码错误，未获取到
                    driver.find_element(by='xpath', value='//*[@id="app"]/div/div[1]/div[2]/form/div[2]/div/div/span/div/div[2]/a').click()  # 再次发送
                elif result == 'password update success':   #修改成功
                    print('还原密码成功'.center(60, '-'))
                    time.sleep(2)
                    break
            elif info == 'Verification code has been sent. Please do not click again!':
                print('尝试快速需改，使用上次验证码进行尝试')
                driver.find_element(by='id', value='horizontal_login_code').send_keys(Keys.CONTROL, 'a')  # 输入验证码
                driver.find_element(by='id', value='horizontal_login_code').send_keys(code)  # 输入验证码
                driver.find_element(by='class name', value='atn-btn-orange.ant-btn.ant-btn-lg.ant-btn-block').click()  # 点击提交
                time.sleep(2)
                result = driver.find_element(by='xpath', value='/html/body/div[2]/span/div/div/div/span').text  # 获取提交后的文本提示
                print(f'提交验证码后提示为{result}')

                if result == 'password update success':  # 修改成功
                    print('还原密码成功'.center(60, '-'))
                    time.sleep(2)
                    break
                else:       # 验证码错误，未获取到
                    print('重复发送，等待一分钟')
                    time.sleep(60)
                    driver.find_element(by='css selector', value='#app > div > div.login-form-wrap > div.login-form.margin-bottom > form > div:nth-child(2) > div > '
                                                                 'div > span > div > div:nth-child(2) > a').click()  # 再次发送
                    print('点击发送成功')
                    WebDriverWait(driver,15,0.2).until(lambda x:x.find_element(by='xpath',value='/html/body/div[2]/span/div/div/div/span'))


    def test(self):
        useraccount = random.choice(['a979172251@163.com', 'a9791722511@126.com', 'a9791722511@163.com', 'a97917225111@163.com', 'a979172251@126.com'])
        print(useraccount)

        # 登录的会话获取

    def login_sess(self):
        sess = requests.session()

        ran_13 = random.randint(1111111111111, 9999999999999)
        ran_10 = random.randint(111111111, 9999999999)
        url1 = f"http://18.118.13.94:8080/jeecg-boot/sys/randomImage/{ran_13}?_t={ran_10}"
        sess.get(url=url1)

        URL = "http://18.118.13.94:8080/jeecg-boot/sys/login"
        header = {'Host': '18.118.13.94:8080',
                  'Connection': 'keep-alive',
                  'Content-Length': '103',
                  'Accept': 'application/json,text/plain,*/*',
                  'tenant-id': '0',
                  'User-Agent': 'Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,'
                                'likeGecko)Chrome/98.0.4758.80Safari/537.36Edg/98.0.1108.43',
                  'Content-Type': 'application/json',
                  'Origin': 'http://18.118.13.94',
                  'Referer': 'http://18.118.13.94/',
                  'Accept-Encoding': 'gzip,deflate',
                  'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6'}
        data = f'{{"username":"test","password":"Xx.888888","captcha":"0000","checkKey":"{ran_13}","remember_me' \
               f'":"true"}} '
        res = sess.post(url=URL, data=data, headers=header)
        token = res.json()['result']['token']
        return sess, token



if __name__ == '__main__':
    a = Common()
    # a.change_password(driver=webdriver.Chrome(),useraccount='a97917225111@163.com',password='a123456',code=0000)
    # a.test()
    a.get_Request_Return()