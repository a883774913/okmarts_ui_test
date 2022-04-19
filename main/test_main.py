

import allure
import pytest

from okmarts_ui_test.data.get_data import Get_Data
from okmarts_ui_test.mode.login import Login

class Test_Main:
    infos = Get_Data().get_data()
    case_infos = infos[0]
    casename_infos = infos[1]


    @allure.feature('登录')
    @pytest.mark.parametrize('Parameter',case_infos['login'],ids=casename_infos['login'])
    def test_login(self,Parameter):
        allure.dynamic.title(Parameter['casename'])  # 测试用例名称
        Login().login(Parameter)


