import allure
import pytest

from okmarts_ui_test.common.common import Common
from okmarts_ui_test.data.get_data import Get_Data
from okmarts_ui_test.mode.login import Login
from okmarts_ui_test.mode.register import Regist


class Test_Main:
    infos = Get_Data().get_data(filepath='../data/UI自动化用测试用例.xlsx')
    case_infos = infos[0]
    casename_infos = infos[1]

    # 前置条件
    def setup_class(self):
        ...

    def teardown_class(self):
        Common().close_browser()

    @allure.feature('登录')
    @pytest.mark.parametrize('Parameter', case_infos['login'], ids=casename_infos['login'])
    def test_login(self, Parameter, driver):
        allure.dynamic.title(Parameter['casename'])  # 测试用例名称
        Login().login(Parameter, driver)

    @allure.feature('注册')
    @pytest.mark.parametrize('Parameter', case_infos['registe'], ids=casename_infos['registe'])
    def test_regist(self, Parameter, driver):
        allure.dynamic.title(Parameter['casename'])  # 测试用例名称
        Regist().regist(Parameter, driver)
