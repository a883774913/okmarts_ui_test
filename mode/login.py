import time
from okmarts_ui_test.common.common import Common

class Login:

    def login(self, Parameter,dr):
        print(Parameter)
        casename = Parameter['casename']
        mode = Parameter['mode']
        data = Parameter['data'].split('\n')
        print(data)
        userAccount = data[0].split('=')[-1]
        password = data[1].split('=')[-1]
        assert_way = Parameter['assert_way']
        result = Parameter['result']

        if casename == '输入错误密码登录失败':
            userAccount = Common().random_account()[0]

        dr.get('http://18.118.13.94:81')
        time.sleep(1)
        Common().Restore_environment(dr)
        dr.find_element(by='xpath', value='//*[@id="app"]/div/div[1]/div/div[2]/div[3]/div[1]/span').click()
        time.sleep(1)
        dr.find_element(by='id', value='horizontal_login_userAccount').send_keys(userAccount)
        dr.find_element(by='id', value='horizontal_login_password').send_keys(password)
        dr.find_element(by='class name', value='atn-btn-orange.ant-btn.ant-btn-lg.ant-btn-block').click()
        time.sleep(2)
        name = dr.find_element(by=f"{assert_way.split('=',1)[0]}", value=f"{assert_way.split('=',1)[1]}").text
        print(name)
        assert name != f"{result}"



