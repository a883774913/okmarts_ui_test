
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

        print(General_table['address'])
        print(General_for_casename['address'])
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
