
import xlrd

class Get_Data:

    def get_data(self,filepath):
        book = xlrd.open_workbook(filepath)
        sheet = book.sheet_by_name('Sheet1')
        General_table = {}      #用于存放用例数据集合
        General_for_casename = {}

        login_casename = []
        login_cases_list = []   #登录用例集合

        registe_casename = []  #注册用例名称集合
        registe_cases_list = [] #注册用例集合

        forget_casename = []        #忘记密码用例名称集合
        forget_cases_list =  []     #忘记密码用例集合

        help_center_casename = []   #帮助中心用例名称集合
        help_center_case_list = []  #帮助中心用例集合

        navigation_bar_casename = []    #导航栏用例名称集合
        navigation_bar_case_list = []   #导航栏用例集合

        address_casename = []           #地址管理模块用例名称集合
        address_case_list = []          #地址管理模块用例集合

        my_order_casename = []          #我的订单用例名称集合
        my_order_case_list = []         #我的订单用例集合

        personal_center_casename = []            #个人中心资料修改用例名称集合
        personal_case_list = []                    #个人中心资料修改用例集合

        shop_car_casename = []          #购物车模块用例名称集合
        shop_car_case_list = []         #购物车模块测试用例集合

        banner_casename = []            #广告位用例名称集合
        banner_case_list = []           #广告位用例集合

        sign_casename = []              #签到模块用例名称集合
        sign_case_list = []             #签到模块用例集合

        conpons_casename = []           #优惠券用例名称集合
        conpons_case_list = []          #优惠券用例集合

        change_password_casename = []       #修改密码用例名称集合
        change_password_case_list = []      #修改密码用例集合

        search_casename = []            #搜索用例名称集合
        search_case_list = []           #搜索用例集合

        for i in range(1,sheet.nrows):
            dicts = {}
            value = sheet.row_values(i)
            case_no = value[0]
            casename = value[1]
            mode  = value[2]
            data = value[4]
            assert_way = value[5]
            result = value[6]

            if mode == '登录':
                self.get_list(dicts,login_cases_list,case_no,casename,mode,data,assert_way,result)
                login_casename.append(casename)
            if mode == '注册':
                self.get_list(dicts,registe_cases_list,case_no,casename,mode,data,assert_way,result)
                registe_casename.append(casename)
            if mode == '忘记密码':
                self.get_list(dicts,forget_cases_list,case_no,casename,mode,data,assert_way,result)
                forget_casename.append(casename)
            if mode == '帮助中心' :
                self.get_list(dicts,help_center_case_list,case_no,casename,mode,data,assert_way,result)
                help_center_casename.append(casename)
            if mode == '导航栏':
                self.get_list(dicts,navigation_bar_case_list,case_no,casename,mode,data,assert_way,result)
                navigation_bar_casename.append(casename)
            if mode == '地址管理':
                self.get_list(dicts,address_case_list,case_no,casename,mode,data,assert_way,result)
                address_casename.append(casename)
            if mode == '订单管理':
                self.get_list(dicts,my_order_case_list,case_no,casename,mode,data,assert_way,result)
                my_order_casename.append(casename)
            if mode == '个人信息修改':
                self.get_list(dicts,personal_case_list,case_no,casename,mode,data,assert_way,result)
                personal_center_casename.append(casename)
            if mode == '购物车':
                self.get_list(dicts,shop_car_case_list,case_no,casename,mode,data,assert_way,result)
                shop_car_casename.append(casename)
            if mode == '广告位':
                self.get_list(dicts,banner_case_list,case_no,casename,mode,data,assert_way,result)
                banner_casename.append(casename)
            if mode == '签到':
                self.get_list(dicts, sign_case_list, case_no, casename, mode, data, assert_way, result)
                sign_casename.append(casename)
            if mode == '优惠券':
                self.get_list(dicts, conpons_case_list, case_no, casename, mode, data, assert_way, result)
                conpons_casename.append(casename)
            if mode == '修改密码':
                self.get_list(dicts, change_password_case_list, case_no, casename, mode, data, assert_way, result)
                change_password_casename.append(casename)
            if mode == '搜索':
                self.get_list(dicts, search_case_list, case_no, casename, mode, data, assert_way, result)
                search_casename.append(casename)


        General_for_casename['login'] = login_casename
        General_table['login'] = login_cases_list

        General_for_casename['registe'] = registe_casename
        General_table["registe"] = registe_cases_list

        General_for_casename['forget'] = forget_casename
        General_table['forget'] = forget_cases_list

        General_for_casename['help_center'] = help_center_casename
        General_table['help_center'] = help_center_case_list

        General_for_casename['navigation_bar'] = navigation_bar_casename
        General_table['navigation_bar'] = navigation_bar_case_list

        General_for_casename['address'] = address_casename
        General_table['address'] = address_case_list

        General_for_casename['my_order'] = my_order_casename
        General_table["my_order"] = my_order_case_list

        General_for_casename['personal_center'] = personal_center_casename
        General_table['personal_center'] = personal_case_list

        General_for_casename['shop_car'] = shop_car_casename
        General_table['shop_car'] = shop_car_case_list

        General_for_casename['banner'] = banner_casename
        General_table['banner'] = banner_case_list

        General_for_casename['sign'] = sign_casename
        General_table['sign'] = sign_case_list

        General_for_casename['conpons'] = conpons_casename
        General_table['conpons'] = conpons_case_list

        General_for_casename['change_password'] = change_password_casename
        General_table['change_password'] = change_password_case_list

        General_for_casename['search'] = search_casename
        General_table['search'] = search_case_list

        print(General_table['search'])
        print(General_for_casename['search'])
        return General_table,General_for_casename

    def get_list(self,dicts:dict,lists:list,case_no,casename,mode,data,assert_way,result):
        dicts['case_no'] = case_no
        dicts['casename'] = casename
        dicts['mode'] = mode
        dicts['data'] = data
        dicts['assert_way'] = assert_way
        dicts['result'] = result
        lists.append(dicts)




if __name__ == '__main__':
    a = Get_Data()
    a.get_data(filepath='./UI自动化用测试用例.xlsx')
