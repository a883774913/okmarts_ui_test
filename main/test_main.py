import allure
import pytest

from okmarts_ui_test.common.common import Common
from okmarts_ui_test.data.get_data import Get_Data
from okmarts_ui_test.mode.Personal_Center import Personal_Center
from okmarts_ui_test.mode.address import Address
from okmarts_ui_test.mode.banner import Banner
from okmarts_ui_test.mode.forget_password import Forget_Password
from okmarts_ui_test.mode.help_center import Help_Center
from okmarts_ui_test.mode.login import Login
from okmarts_ui_test.mode.my_order import My_Order
from okmarts_ui_test.mode.navigation_bar import Navigation_Bar
from okmarts_ui_test.mode.register import Regist
from okmarts_ui_test.mode.shop_car import Shop_Car


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

    @allure.feature('忘记密码')
    @pytest.mark.parametrize('Parameter', case_infos['forget'], ids=casename_infos['forget'])
    def test_forget_password(self,driver,Parameter):
        allure.dynamic.title(Parameter['casename'])
        Forget_Password().forget_password(driver,Parameter)

    @allure.feature('帮助中心')
    @pytest.mark.parametrize('Parameter', case_infos['help_center'], ids=casename_infos['help_center'])
    def test_help_center(self,driver,Parameter):
        allure.dynamic.title(Parameter['casename'])
        Help_Center().help_center(driver,Parameter)

    @allure.feature('导航栏')
    @pytest.mark.parametrize('Parameter', case_infos['navigation_bar'], ids=casename_infos['navigation_bar'])
    def test_navigation_bar(self,driver,Parameter):
        allure.dynamic.title(Parameter['casename'])
        Navigation_Bar().navigation_bar(driver,Parameter)


    @allure.feature('地址管理')
    @pytest.mark.parametrize('Parameter', case_infos['address'], ids=casename_infos['address'])
    def test_address(self,driver,Parameter):
        allure.dynamic.title(Parameter['casename'])
        Address().address(driver,Parameter)

    @allure.feature('订单管理')
    @pytest.mark.parametrize('Parameter', case_infos['my_order'], ids=casename_infos['my_order'])
    def test_my_order(self, driver, Parameter):
        allure.dynamic.title(Parameter['casename'])
        My_Order().my_order(driver,Parameter)

    @allure.feature('个人资料修改')
    @pytest.mark.parametrize('Parameter', case_infos['personal_center'], ids=casename_infos['personal_center'])
    def test_personal_center(self,driver,Parameter):
        allure.dynamic.title(Parameter['casename'])
        Personal_Center().person_center(driver,Parameter)

    @allure.feature('购物车')
    @pytest.mark.parametrize('Parameter', case_infos['shop_car'], ids=casename_infos['shop_car'])
    def test_shop_car(self,driver,Parameter):
        allure.dynamic.title(Parameter['casename'])
        Shop_Car().shop_car(driver,Parameter)

    @allure.feature('广告位')
    @pytest.mark.parametrize('Parameter', case_infos['banner'], ids=casename_infos['banner'])
    def test_banner(self, driver, Parameter):
        allure.dynamic.title(Parameter['casename'])
        Banner().banner(driver,Parameter)

