# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2022/4/27 11:08
# Desc: BluePrint测试用例

import pytest, os
from selenium.webdriver.common.by import By
from pages.BluePrint import BluePrint
from selenium import webdriver
from time import sleep


class Test_BluePrint():

    def setup_class(self):
        self.driver = webdriver.Chrome()
        self.bp = BluePrint(self.driver)
        self.bp.open_blueprint()

    def teardown_class(self):
        sleep(3)
        self.driver.quit()

    @pytest.mark.parametrize('user,password', [('lin82726142@163.com', '123123Qq.')])
    def test_01_login(self, user, password):
        """ 正确的账户密码登陆 """
        self.bp.login(user, password)
        assert self.bp.element_display((By.XPATH, '//*[@class="logout pointer"]'))

    @pytest.mark.parametrize('user,password', [('xxx@163.com', '123123Qq.')])
    def test_02_login_failure(self, user, password):
        """ 错误的账户密码登陆 """
        self.bp.login(user, password)
        assert self.bp.element_display((By.XPATH, "//div[@*='ant-form-explain']"))

    def test_03_site(self):
        """ 场地检查 """
        self.bp.login()
        site_num = self.bp.site_list()
        assert site_num >= 2

    def test_04_select(self):
        pass


if __name__ == '__main__':
    pytest.main()
    os.system(r"allure generate D:\AutomationLogreport -o ../report --clean")
    print(1)
