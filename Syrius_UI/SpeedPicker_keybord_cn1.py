# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2021/12/9 19:17

import copy
import re
from time import sleep
from base.base_page import TestKey
from selenium.webdriver.common.by import By
from appium import webdriver
from Syrius_API.flagship.SendOrder import send_order
from base.common import *
from utils.file_reader import YamlReader
from utils.mylog import Logger


def pad_ip():
    num = int(__file__.split('\\')[-1].split('.')[0].split('cn')[-1]) - 1  # 序号从0开始
    devices_ls = get_devices()
    try:
        return devices_ls[num].replace(':5555', '')  # 只拿PAD的IP
    except:
        log.error("获取设备UDID失败了，检查一下。", level='WARNING', color='r')


# 日志目录，文件。
file = r"D:\AutomationLog\\" + get_date() + '_' + pad_ip() + '.txt'
log = Logger(name='SpeedPicker', file=file)


class GGR():
    def __init__(self):
        pass

    def browser(self, devices='xxx', port='4723', platformversion='8'):
        app_data = {
            "platformName": "Android",  # 平台
            "udid": devices,
            "platformVersion": platformversion,  # 注意调试平板的安卓版本
            "deviceName": 'c5',  # 注意调试平板的IP,参数化来控制多设备。
            "apppackage": "com.syriusrobotics.platform.launcher",  # 包名
            "appActivity": "com.syriusrobotics.platform.launcher/com.syriusrobotics.platform.jarvis.MainFlutterActivity",
            "noReset": True,  # 不要重置
            # "unicodeKeyboard": True,  # 不会吊起键盘。
            # "resetKeyboard": True,  # 恢复键盘
            'newCommandTimeout': 30000,  # 命令超时时间。给长一点
            'automationName': 'UiAutomator2'  # 可能是这里导致的常断开
        }
        br = webdriver.Remote(f"http://localhost:{port}", app_data)
        driver = TestKey(br, file=file)  # 传入脚本日志写在哪，确保单个机器人写的日志都集中在一起。
        return driver


class SpeedPicker:

    def __init__(self):
        self.driver = self.init_driver()
        # sleep(10)  # 做一个长等待，没办法。加载慢。
        self.view = (By.XPATH, '//android.view.View')
        self.image = (By.XPATH, '//android.widget.ImageView')
        self.widget_text = (By.XPATH, '//android.widget.TextView')  # K11桌面的组件和新版GGR的悬浮窗，部分界面文本组件。
        self.notify()  # 刷新一些提醒，避免遗漏配置。
        self.non_count = 0  # 界面抓到异常信息的计数器.
        self.siteid = 202  # 默认是备用场地。
        self.start_time = time.time()  # 一个初始的计时器。
        self.time_count = [0]  # 检查文本时的时间计时列表。
        self.sp_text = []
        self.shoot_text = []
        self.useless_text = self.get_config()['useless_text']

    def init_driver(self):
        pad_ip = self.device_num()[0]  # 10.111.150.202:5555 这种格式.
        appium_port = self.device_num()[1] or '4725'
        # 在这里填入安卓版本,避免跑不起来.
        browser = GGR().browser(devices=pad_ip, platformversion=get_android_version(pad_ip),
                                port=appium_port)  # 自己获取安卓版本
        log.info(f"脚本当前连接的平板:{pad_ip}，安卓版本：{get_android_version(pad_ip)}，Appium端口:{appium_port}")
        return browser

    def reset_timer(self):
        self.start_time = time.time()  # 一个初始的计时器。
        self.time_count = [0]

    def notify(self):
        """ 脚本启动的一些注意事项提醒 """
        log.debug("注意事项：\n1.SpeedPicker请开启快速拣货功能。\n2.注意平板连接到此电脑。\n3.注意先启动Appium服务。")

    def device_num(self):
        num = int(__file__.split('\\')[-1].split('.')[0].split('cn')[-1]) - 1  # 序号从0开始
        devices_ls = get_devices()
        try:
            return devices_ls[num], 4725 + num * 5  # 每个设备之间，间隔5个以上
        except:
            log.warning("获取设备UDID失败了，检查一下。")

    def robot_battery(self):
        tmp_text = self.driver.app_elements_text(self.widget_text)
        for i in tmp_text:
            if i.endswith('%') and i.split('%')[0].isdigit():
                log.info(f"当前机器人电量为:{i}")
                return 1
        return 0

    def open_sp(self):
        log.debug(f"脚本启动成功，检查是否需要脚本启动SpeedPicker。")
        # 先判断是否有异常.   更新：异常通知改为系统悬浮窗，appium抓不到。不再检查。
        # if self.err_notify():  # 异常函数会自己报异常.
        #     exit(-404)  # 走不动了,直接停吧.
        # 抓取界面的小程序.
        try:
            desc = self.driver.app_elements_content_desc(self.view)
            if 'SkillSpace' not in ''.join(desc):
                log.debug("当前不在Jarvis Launcher主界面。")
                return
            else:
                log.debug(f"Jarvis Launcher 主界面上的content:{desc}")  # 保留这个打印，记录当时的日期，桌面小程序。
                site_name = re.findall(r"\n(.*?)\nSkill", ''.join(desc))[0]  # 正则提取出场地名称。
                if site_name in ['sz-sqa-test-spare', 'sz-sqa-test']:
                    log.debug(f"获取到当前场地为:{site_name}。")
                    update_yaml('config_file/site_info.yaml', {self.get_filename(): site_name})
                else:
                    log.debug(f"获取到的场地不是sqa测试场地，关闭接口自动派单功能。")
                    update_yaml('config_file/site_info.yaml', {'api_order': False})
                image = self.driver.find_elements(self.image)
                soft_index = self.driver.app_elements_content_desc(self.view)
                installsp = False
                for i in soft_index:
                    if 'SpeedPicker' in i:
                        installsp = True
                        x = i.split('\n')[::-1]
                        sp_index = x.index('SpeedPicker') + 1  # 因为反过来了.从0开始.
                        self.driver.click_one(image[-sp_index])
                        log.info("尚未启动SpeedPicker，即将自动启动SpeedPicker。")
                        sleep(1)
                        tmp_text = self.get_text()
                        for item in tmp_text:
                            if 'version:' in item:
                                log.info(f"SpeedPicker的版本是:{item.split(':')[-1]}")
                                self.wait_moment(item, i=False, without="退出")
                                new_text = self.get_text()
                                if item in new_text and '退出' in new_text:
                                    log.warning(f"发生了一些异常，SpeedPicker不能正常启动:{new_text}")
                                    exit(-404)
                                return
                        # 想办法在启动的时候,走一下更新流程.
                        if self.driver.element_display((By.XPATH, '//*[starts-with(@text,"更新")]')):
                            break
                else:
                    if len(interset(self.get_text(), self.get_config()['sp_text'])) > 1:
                        return
                    if not installsp:
                        log.warning(f"这个设备{self.device_num()[0]}还没有安装SpeedPicker，请先安装。")
        except:
            return

    def update_sp(self):
        self.driver.click_element((By.XPATH, '//*[starts-with(@text,"更新")]'))  # 点击更新,应该跳转skillspace里
        self.driver.click_element((By.XPATH, '//*[@*="更新"]'))
        self.driver.click_element((By.XPATH, '//*[@*="打开"]'), wait=30)  # 下载时间有点长.

    def err_notify(self):
        try:
            notify = self.driver.app_elements_content_desc(self.image, wait=2, where='检查异常通知')  # 不用抓太久.
            if notify:
                for i in notify:
                    if (len(i) > 3 and '机器人' in i) or (len(i) > 3 and '平板' in i):
                        log.info(f"这个设备发生了一些异常:[{i}]，请先恢复异常。")
                        return 1
            else:
                return 0  # 跳出循环
        except:
            return 0  # 异常也跳出循环

    def inputcode(self, code='199103181516'):  # 默认输入万能码
        """ 输入条形码的函数 """
        try:
            self.driver.input_text(locator=(By.XPATH, '//android.widget.EditText'), text=str(code))
            log.debug(f"文本[{code}]输入成功。")
            self.driver.click_element((By.XPATH, '//android.widget.EditText'))  # 再点击一次输入框,才能按回车
            self.driver.press_keyboard()
        except:
            log.warning(f"输入功能，输入{code}失败，请检查。")

    def islosepos(self):
        """检查机器人是否丢失定位,但是重复了."""
        try:
            self.driver.find_elements(
                locator=(By.XPATH, '//android.widget.TextView[contains(@text,"机器人定位丢失")]'),
                wait=1, raise_except=True)
            self.shoot()
            return 1  # return True
        except:
            sleep(0.1)

    def random_trigger(self, israndom=True, n=30, process=''):  # Probability value
        if not israndom:  # 默认开启随机事件
            return 0
        # 获取一个随机数值，选中了，就触发随机事件。
        if n == 0:  # 设置为0，关闭随机事件。
            return 0
        elif n == 1:  # 设置为1，必中事件。
            log.debug(f"{process}流程,随机事件被设置为常开，注意使用。")
            return 1
        elif n >= 2:
            num = random.randint(2, n + 2)  # 1和0被排除，得多加两个。
            if num == n:  # 如果抽中的数和概率值一样,则中奖了.触发随机事件.
                return 1  # return True
        else:
            return 0

    def pause_move(self, time_out=15):  # 不宜过长,省得脚本卡时间,恢复按钮没了.
        """ 暂停移动功能 """
        view_text = self.driver.app_elements_text((By.XPATH, '//android.view.View'))
        wait_time = random.randint(5, time_out)
        if '暂停' in view_text:
            self.driver.click_element((By.XPATH, '//android.view.View[@text="暂停"]'))
            if self.random_trigger(n=50, process='倒计时自动恢复流程'):  # 概率低一点，偶尔看一下即可。
                log.debug(f"触发随机事件，不提前点击恢复按钮，让SpeedPicker暂停倒计时结束后，自行恢复移动。")
                self.wait_moment('恢复')
                log.debug('倒计时结束，SpeedPicker自行恢复移动。注意后续流程是否正常流转。')
                return
            log.info(f"移动过程中，暂停移动[{wait_time}]秒钟。")
            sleep(wait_time)
            try:
                self.driver.click_element((By.XPATH, '//android.view.View[@text="恢复"]'))
                log.info(f"暂停结束，恢复移动。")
                return
            except:
                log.info("恢复按钮消失了，可能是人为点击了。")
                return

    def press_ok(self, num=3, timeout=0.5):
        # log.debug("点击确定流程.")
        # 点击确定按钮
        count = num
        while count > 0:
            try:
                self.driver.click_element((By.XPATH, '//*[@text="确定"]'), wait=timeout)
                break
            except:
                count -= 1
            try:
                self.driver.click_element((By.XPATH, '//*[@text="完成"]'), wait=timeout)
                break
            except:
                count -= 1
                break

    def input_error(self, code):
        # Used to verify the input error barcode. The premise of execution is that the input box pops up.
        err_num = str(random.randint(0, 1000))
        self.inputcode(code=str(code) + err_num)  # Add a random number to form an error barcode.
        log.info("随机事件，输入一个[错误的]条码。")

    def get_text(self, ele='', wait=3, raise_except=False, ):  # 3s左右合理,有些流程跳转时,会转圈一会儿.
        if not ele:
            ele = self.view
        count = 20  # 有个限制.
        while count > 0:
            count -= 1  # 避免死循环
            view_ls = self.driver.app_elements_text((By.XPATH, '//*'), wait)  # 拿到异常类型的文本。文本也是view.View类型的。
            try:
                view_ls = [i for i in view_ls if i != '']  # 去重。会抓到空文本。
                if view_ls:  # 抓到才出去.在sp里,必定是会有文本页面的.
                    list_remove(view_ls, self.useless_text)
                    return view_ls
                else:
                    if count % 10 == 0:  # 偶尔刷新一次.
                        # 判断是不是在Jarvis主界面.
                        try:
                            tmp_desc = self.driver.app_elements_content_desc(locator=self.view)
                            if 'SkillSpace' in ''.join(tmp_desc):
                                self.open_sp()
                        except:
                            pass  # The function needs to be improved
                        log.info("当前页面没抓到文本，如果持续刷新这个日志，请前往检查一下。")
                        self.is_other_page()  # 检查一下,是否退出了SP界面.
                        return  # 跳出去
            except TypeError:
                log.debug("抓取文本发生类型错误异常，检查是否退出SP界面了。")
                self.is_other_page()
                if self.random_trigger(n=60, process='主线程日志打印'):
                    log.debug(f"随机刷日志， 脚本仍然在抓取文本中，当前可能拿到了一些不符合要求的:{view_ls}")
                    sleep(10)
                    break  # 尝试退出一下,因为总会重复刷这个日志.
                if raise_except:
                    raise just_err
                sleep(5)
            except Exception as e:
                log.info(f"抓取文本，出现了一些别的异常:{e}")
                return  # 跳出去
        if count == 0:
            log.info(f"这个设备:{self.device_num()[0]}有一段时间没抓到文本了，去检查一下。")
            sleep(10)  # 这里也要睡眠一下，避免刷日志太快了。
            return  # 跳出去

    def K11_text(self):
        while True:
            text = self.driver.app_elements_text(self.widget_text)
            if text:
                return text

    def is_other_page(self):
        log.debug("检查是否进入其他界面了。")
        if not check_app(device=self.device_num()[0], appname='com.syriusrobotics.platform.launcher'):
            log.warning("设备的GoGoReady似乎闪退了。")
            self.shoot()
            self.start_GGR()
            return 1
        try:
            if self.driver.element_display((By.XPATH, '//*[contains(content-desc,"配置信息")]')):
                log.info("机器人正在同步配置信息，请稍后...")
                sleep(10)
            elif self.driver.element_display((By.XPATH, '//*[starts-with(@text,"/sdcard/log/")]')):
                log.info("机器人正在收集GoGoReady日志，请稍等...")
                while True:
                    if self.driver.element_display((By.XPATH, '//*[starts-with(@text,"/sdcard/log/")]')):
                        sleep(3)
                    else:
                        break
                sleep(10)
            elif self.driver.element_display((By.XPATH, '//*[contains(@content-desc,"上传机器人日志")]')):
                log.info("正在上传机器人日志，请稍后...")
                while True:
                    if self.driver.element_display((By.XPATH, '//*[contains(@content-desc,"日志上传完成")]')):
                        log.debug("机器人日志已上传完成，请自行前往解决异常，恢复机器人移动。")
                        self.shoot(just_shoot=True)
                        log.debug("即将通过脚本返回Jarvis主界面，请确保机器人无异常产生。保证业务正常进行。")
                        for i in range(3):
                            os.system(
                                f"adb -s {self.device_num()[0]} shell input keyevent 4")  # 连续3次,才能返回到桌面.到桌面,再按一次.也不会到系统桌面
                            sleep(1)
                        break  # 返回完了,退出去
                    elif self.driver.element_display((By.XPATH, '//*[contains(@content-desc,"请稍后")]')):
                        schedule = self.driver.app_elements_content_desc((By.XPATH, '//*'))
                        for i in schedule:
                            if i.startswith('请稍后'):
                                log.debug(f"日志正在上传，{i}...")
                        sleep(3)
                    elif self.driver.element_display((By.XPATH, '//*[contains(@content-desc,"正在准备日志文件")]')):
                        log.debug(f"下位机日志准备中...")  # 转圈的准备过程
                        sleep(60)
                    # exit(100)
            elif self.driver.element_display((By.XPATH, '//*[contains(@content-desc,"SkillSpace")]')):
                log.info("机器人在Javis Launcher主界面，尝试重新打开SpeedPicker。")
                # if self.err_notify():  # 这个已经查不到了，退出检测。
                #     return
                self.open_sp()
            # elif self.driver.app_elements_content_desc((By.XPATH, '//*[contains(@content-desc,"完成")]')):
            #     self.driver.click_element((By.XPATH, '//*[contains(@content-desc,"完成")]'))
            #     log.debug("同步配置完成，点击完成按钮。")
            # elif self.driver.app_elements_content_desc((By.XPATH, '//*[@content-desc="设置"]')):
            #     log.debug("在GoGoReady的设置界面。")
            #     sleep(5)
            else:
                sleep(5)
        except Exception as e:
            self.non_count += 1
            sleep(5)  # 一般是干掉GGR了. 刷慢一点.
            if self.non_count >= 5:
                log.debug(f"连续5次抓不到文本，可能是Appium通讯断了。当前异常:{e}")
                raise just_err(message="通讯可能出问题了")
        try:
            x = self.driver.app_elements_content_desc((By.XPATH, '//*'))
            view_text = self.get_text()
            if len(interset(view_text, self.get_text())) == 0:
                log.warning("SpeedPicker可能白屏了。或者进入别的界面了。请检查。")
                self.shoot()
            log.warning(f"抓到了什么奇怪的content:{x}")
            if len(interset(self.get_config()['jarvis_soft'], ''.join(x).split('\n'))) > 1:
                log.debug('异常返回了Jarvis主界面,脚本重启SpeedPicker。')
                self.open_sp()
            # elif '正在同步场地配置' in x:
            #     log.debug("正在同步场地配置，请等待")
            #     while True:
            #         if self.driver.element_display((By.XPATH, '//*[@starts-with(@content-desc,"完成")]')):
            #             log.debug("云端配置同步完成。")
            #             self.driver.click_element((By.XPATH, '//*[@starts-with(@content-desc,"完成")]'))
            #             break
            #         else:
            #             sleep(3)
            # elif len(interset(['机器人定位丢失', '收起'], x)) == 2:
            #     log.warning("机器人丢失定位。")
            #     self.shoot()


        except Exception as e:
            log.debug(f"content-desc也没有找到，可能是退出GoGoReady了。发生异常:{e}")
            sleep(5)

    def start_GGR(self):
        log.warning("GoGoReady没有在运行.准备启动GoGoReady.请等待GoGoReady启动完成.约30s...")
        os.system(f'adb -s {self.device_num()[0]} shell am start -n '
                  f'"com.syriusrobotics.platform.launcher/com.syriusrobotics.platform.jarvis.SplashActivity"'
                  f' -a android.intent.action.MAIN -c android.intent.category.LAUNCHER')
        sleep(30)  # 启动加载需要时间,不能直接起脚本.
        while True:
            if self.robot_battery():
                log.debug(f"获取机器人电量成功，完成连接。")
                break
            else:
                log.debug(f"暂未获取到电量信息，请等待。")
                sleep(10)

    def report_err(self, err=''):
        # 进入异常上报流程的入口。
        view_ls = self.get_text()
        if view_ls[0] == '异常上报':
            log.info("当前在异常上报流程。")
            self.do_err(err)
        else:
            try:
                self.driver.click_element((By.XPATH, '//android.widget.Image[@enabled="true"]'), wait=3,
                                          raise_except=True)
                # self.click_view_text("异常上报")  # 不能这么做,点进去了,异常上报还是在文本中.
                self.do_err(err)
            except:
                log.warning("异常上报流程，点击上报按钮出现了一些问题。")
                return

    def do_err(self, err=''):
        # 上报异常的冗余函数.
        sleep(1)  # 点太快了。脚本进来时，文本还没刷新。做个等待。
        tmp_text = self.get_text()
        if '异常上报' not in tmp_text:
            log.warning("当前在异常上报流程，但是不在异常上报界面了。去检查一下。")
            return
        if err:
            self.driver.click_one(self.driver.find_element((By.XPATH, f'//android.view.View[@text="{err}"]')))
            self.press_ok(timeout=2)  #
            return
        view_ls = tmp_text
        list_remove(view_ls, ['speed_picker', '异常上报'])  # 把这俩去掉
        log.debug(f"当前可上报异常：{view_ls}")
        err_type = random.choice(view_ls)  # 随机选的一个异常类型
        log.debug(f"本次随机上报的异常是:{err_type}")
        self.driver.click_one(self.driver.find_element((By.XPATH, '//android.view.View[@text="%s"]' % err_type)))
        count = 3
        while count > 0:
            try:
                view_ls2 = self.get_text()
                err_type2 = '其他' if err_type == '其他' else re.findall("确定(.*?)吗", ''.join(view_ls2))[0]  # 拿到的异常
                log.debug(f"确定上报[{err_type2}]异常吗？")  # 询问弹窗.再次确认弹窗询问的异常和选择的是否一致.
                if err_type2 == err_type or err_type == '其他' or '确定' in self.get_text():  # [其他]异常,询问框不一致.
                    if '上报' in self.get_text():  # 其他异常，要走其他流程了。
                        reason = random.choice(self.get_config()['other_err_reason'])  # 随机选一个异常理由。
                        if self.random_trigger(n=5):  # 这里就不用配置化了。
                            reason = (reason * 10)[:128]  # 长度加长一下,也截取前128位。
                            log.debug(f"本次上报的[其他]类型异常原因是：{reason}")
                        self.inputcode(code=reason)
                        self.click_view_text("上报")
                        if self.page_check(timeout=6, pagename='上报其他异常', text='上报', new_text='前往',
                                           new_text2='输入', is_shoot=True):
                            return 1
                    # self.driver.click_one(self.driver.find_elements(self.view)[-1])  # 最后一个view元素是'确定'按钮.
                    self.press_ok(timeout=1)  # 这里已经点击了确定，为什么还会卡呢？
                    if '确定' not in self.get_text():  # 跳转流程了.
                        # self.wait_moment(err_type)  # 用这个方法应该可以,需要验证一下.
                        log.info(f"上报异常:[{err_type}]成功。")
                        # 页面检查需要检查特征文本,原因:上报[载物箱类型不符]后,15s内,要是刷到了异常区.可能有部分文本重叠.
                        # 上报完异常，两个状态：1.原地继续拣货--特征文本，‘异常上报’还在。2.移动了。
                        if self.page_check(timeout=6, pagename='异常上报', is_shoot=True, text='异常上报', new_text='输入'
                                , new_text2='输入'):
                            return 1
                    else:
                        tmp_text = self.get_text()
                        log.warning(f"上报异常流程，好像发生了什么异常，去看看吧。此时的页面:{tmp_text}")
                        if '拣货异常' in tmp_text:
                            log.debug(f"到达了异常点，异常上报流程正常流转。")
                        else:
                            self.shoot()
                sleep(1)  # 暂停一下.
                count -= 1
            except:
                count -= 1
                sleep(1)
        if err_type == '载具不合适':
            self.wait_moment('前往')
            while True:
                try:
                    self.click_view_text('完成', wait=2)
                    log.info("安装载具完成。")
                    break
                except:
                    count -= 1
                    sleep(1)

    def wait_moment(self, text, wait=3, timeout=2, i=True, without=None):
        # 持续去抓某个文本，直到这个文本不再这个页面了。说明流程变了。
        # 这里可能是影响效率的地方，想办法怎么优化一下。
        log.debug(f"持续检查文本[{text}]是否还在当前页面。")
        count = self.time_count
        err = 20
        err_num = copy.copy(err)  # err 一直在自减，这里要拷贝一下。
        while err > 0:
            try:
                view_ls = self.get_text(wait=wait, raise_except=True)  # 不用太频繁.
                if view_ls:  # 居然还有空的情况，干。
                    if text in view_ls:
                        if self.random_trigger(n=20, process='持续抓文本'):
                            err -= 1  # 有时候可能卡流程,这里也做一个跳出检测
                            sleep(timeout)
                            if i:
                                log.debug(f"调试功能，持续抓取文本:[{text}]中。")
                        elif text == '前往':
                            if '恢复' in view_ls:
                                sleep(5)  # 有时候人要推,给点时间.
                                self.click_view_text('恢复')
                        elif '关闭' in view_ls:
                            log.debug(f"出现关闭按钮，页面信息:{view_ls}")
                            self.click_view_text("关闭")
                        elif '重试' in view_ls:  # 机器人无响应.结果上传失败.
                            log.warning(f"出现了重试按钮，此时的界面文本:{view_ls}")
                            self.driver.tap((By.XPATH, '//*[@text="重试"]'))
                        elif without:
                            # if without text display,break loop
                            if self.driver.element_display((By.XPATH, f'//*[@text="{without}"]')):
                                log.debug(f"文本[{without}]刷新。 停止检查[{text}]。")
                                self.reset_timer()
                                return
                        elif '等待任务中' in view_ls:
                            wait_time = 20
                            sleep(wait_time)
                            if '等待任务中' in self.get_text():
                                if read_yaml('config_file/site_info.yaml', 'api_order'):
                                    log.debug(f"持续等待{wait_time}s，机器人仍然等待任务，且开启了接口发送订单功能。")
                                    self.api_order()
                                    sleep(40)
                        elif self.islosepos():
                            log.warning("机器人丢失定位。")
                            self.shoot()
                            self.reset_timer()
                            return
                        sleep(1)  # 等待时间不能太长。
                        minutes = (time.time() - self.start_time) // 60 or 0  # or 0 只是为了下面这行不报黄。
                        if minutes % 5 == 0 and minutes not in count:  # 每5分钟上报一次.
                            count.append(minutes)
                            log.warning(
                                f"当前页面超过{minutes}分钟没有变化了，请检查是否发生了什么异常情况。")
                            self.shoot()
                            # self.err_notify()
                            return  # 出问题了，也跳出流程，等着回来吧。回来之前，不要重置计时器。
                    else:
                        self.reset_timer()
                        return  # 抓不到重复的文本了。跳出循环。不能是break,会执行后面的if else
                else:
                    if self.random_trigger(n=60, process='抓文本异常捕捉'):
                        log.info(f"获取到了None文本，为什么？")
                        self.shoot()
                    err -= 1  # 这种情况,也给他跳出循环.
                    sleep(timeout)
            except TypeError:
                pass  # 类型错误,前提是已经抓到元素,那么就是空文本问题,这种情况,不要跳出去.继续抓.
            except Exception as e:
                log.warning(f"持续获取的文本的流程，发生了一些异常:{e}")  # 暂时先保留,现场这里问题是真的多.
                self.shoot()
                if not e:
                    self.shoot()
                    raise just_err("抓文本流程，拿到空异常。")
                err -= 1
                sleep(1)
        if text == '请到此处附近':
            log.warning("卡在推荐点位界面了，去检查一下吧!!!!!!")
            self.shoot()
        else:
            log.debug(f"持续检查文本，超过{err_num}次，都没有跳出检查函数。检查一下页面吧!当前页面:{self.get_text()}")
        if self.time_count.__len__() >= 12:
            log.warning(f"SpeedPicker超过{self.time_count[-1]}分钟页面无变化，退出脚本，请前往检查一下。")

    def page_check(self, timeout=30, pagename='', is_shoot=False, text='', new_text='', new_text2='', is_quit=True):
        # 暂时就这么设计，如果跳转的文本过多，则使用**kwargs，代替多参数。
        total_time = copy.copy(timeout)
        start = time.time()
        view_text = self.get_text()  # 先抓一个当前页面文本.
        log.debug(f'[{pagename}]进入检查是否卡屏流程，超时时间:{timeout}s。')
        # view_content =
        while (time.time() - start) < timeout:
            tmp_text = self.get_text()
            if text_in_list('附近', tmp_text):
                log.debug(f"推荐点位信息：{tmp_text}")
                try:
                    locate = tmp_text[el_index("请到此处附近", tmp_text) + 1]
                    log.debug(f'抓取到推荐点位：{locate}')
                except IndexError:
                    log.warning(f"发生异常：索引错误。推荐点位页面，抓取到特征文本，但缺失了点位文本。")
                    log.debug(f"再次抓取推荐点，查看是否抓取到：{self.get_text()}")
            if view_text == tmp_text:
                sleep(1)
                if text not in tmp_text and text:
                    log.debug(f"卡屏判断1-特征文本：[{text}]已经不在{pagename}页面，判定界面已跳转，程序未卡屏。")
                    return 1  # 特征文本不在界面内了.也可以跳过了.
                elif (new_text, new_text2) and interset((new_text, new_text2), tmp_text):
                    log.debug(f"卡屏判断2-特征文本：[{new_text, new_text2}],出现在当前界面。判定界面已跳转，程序未卡屏。")
                    return 1
                elif '当前作业被取消' in tmp_text:
                    log.info("当前作业被取消了。")
                    self.click_view_text('好')
                    return 1
            else:
                log.debug(f"卡屏判断3-特征文本：[{text}]已经不在{pagename}页面，判定界面已跳转，程序未卡屏。")
                return 1  # 页面变化了.
        if pagename == "拣货完成":
            tmp_text = self.get_text()
            if '/' in tmp_text[:-1]:
                index_1 = tmp_text.index('/')
                if tmp_text[index_1 - 1].isdigit() and tmp_text[index_1 + 1].isdigit():
                    log.warning(f"没有开启快速拣货，脚本不能顺利执行。请开启快速拣货，退出脚本。")
                    self.shoot()
                    # exit(-100)
        elif text == "已取下":
            if '上传结果失败' in self.get_text():
                count = self.get_config()['res_report_times']  # 配置化。
                seq = 1
                log.warning(f"当前订单上传结果失败了。尝试重新上传结果[{count}]次。")
                retry_btn = (By.XPATH, '//*[@text="重试"]')
                skip_btn = (By.XPATH, '//*[@text="暂时跳过"]')
                while count:
                    self.driver.click_element(retry_btn)
                    if self.driver.element_display(retry_btn):
                        log.warning(f"第{seq}次重试失败。")
                        seq += 1
                        count -= 1
                    else:
                        log.debug(f"第{seq}次重试上传拣货结果成功，拣货流程正常流转。")
                        return 1
                else:
                    log.warning(f"连续{count}次重试上传均失败，本次尝试暂时跳过本次结果上传。")
                    self.driver.click_element(skip_btn)
                    # 调用自身，可能有点问题。先看看。
                    self.page_check(timeout=10, pagename="拣货结果上报", text="暂时跳过", is_shoot=True,
                                    new_text="前往")

        log.warning(f"超过[{total_time}]s，[{pagename}]页面文本没有变化。可能卡界面了。")
        if is_shoot:
            self.shoot()
        if is_quit:
            exit(-100)

    def click_view_text(self, text, wait=1, count=5, new_text=None, new_element=None, pagename='强点操作'):
        # 强点击,保证点到.
        while count > 0:
            if text not in self.get_text():
                log.info(f"文本:[{text}]并不在页面内，退出强点流程。")
                return
            self.driver.click_element((By.XPATH, f'//*[@text="{text}"]'), wait=wait)
            sleep(2)  # 确定要留足2s钟，不然检测早了。老是会刷点击失败的日志。
            tmp_text = self.get_text(wait=1)
            if text not in tmp_text or new_text in tmp_text:
                log.debug(f"强点击文本:[{text}]成功。")
                return
            elif self.driver.element_display(new_element):
                log.debug(f"强点击文本:[{text}]成功。")
                return
            else:
                log.warning(f"强点操作，点击[{text}]失败。")
                self.page_check(timeout=6, text=text, is_shoot=True, pagename=pagename, is_quit=False)
                count -= 1
        if count == 0:
            self.shoot()

    def wait_for_time(self, timeout=30, n=0):
        if self.random_trigger(n=n, process='超时等待'):
            log.debug(f"进入超时等待，模拟超时未操作。等待时间:{timeout}s。")
            start = time.time()
            while time.time() - start < timeout:  # 用实际时间差来控制这个等待时间。
                view_text = self.get_text(wait=2)  # 这有实际时间做对比，这里无所谓。
                if '超时' in ''.join(view_text):
                    log.warning("出现超时弹窗了，注意检查一下！！！")

    def picking(self, picking_text, target='', checktarget=False, ismove=False):
        # log.debug(f"当前输入法是：")?
        init_loc = {'x': 21, 'y': 1068}
        count = 7
        while True:
            log.debug(f"第{count}次检查。")
            self.click_view_text("扫货品/输入", new_element=(By.XPATH, '//android.widget.EditText'),
                                 pagename="拣货点击输入")  # 点击输入按钮
            loc = self.driver.element_loc((By.XPATH, '//android.widget.EditText'))
            if loc != init_loc:
                log.error(f"键盘没有成功弹起，输入框位置不对。请检查。")
                self.shoot()
                break
            log.debug(f"输入框已弹出，坐标：{loc}")
            # sleep(2)
            self.driver.tap(binlocation=[loc['x'], loc['y'] - 80])
            # sleep(2)
            if not self.driver.element_display((By.XPATH, '//android.widget.EditText')):
                log.debug(f"键盘收起成功。")  # 这个判断，可能不太合理。
            else:
                log.error(f"键盘收起，但输入框没有正常收起。")
                self.shoot()
            # sleep(3)
            count += 1

    def check_time(self):
        while True:
            temp_text = self.get_text()
            if "确定" in ''.join(temp_text):
                log.debug(f"倒计时功能检查:{temp_text}")
            elif '重试' in temp_text:
                self.click_view_text('重试')
                break
            else:
                break

    def go_to(self):
        # self.check_time()  # 放在这里检查一下,页面是否正常退出了.
        self.press_ok()  # 和倒计时功能不能共存,会主动点掉. 当然,要是倒计时点不掉,也能发现新BUG.
        log.info("当前商品拣货完成，检查是否有推荐点。")
        start = time.time()
        while time.time() - start < 6:
            try:
                before = self.get_text(wait=1, raise_except=True)  # 先抓一次前文本.
            except:
                continue
            if text_in_list('附近', before):  # 带有附近的文本，在当前文本里。
                log.debug(f"拿到推荐点位了:{before}")
                try:
                    if '附近' in before[-1]:
                        log.debug(f"这次脚本抓的文本里，没有包含库位信息。再抓一次看看:{self.get_text()}")
                        break
                    log.info(f"抓取到推荐点位--->{before[before.index('请到此处附近') + 1]}")
                    self.wait_moment("请到此处附近")
                    break
                except Exception as e:
                    log.warning(f"增加了点位判断，还是出现了异常{e}。页面文本:{before}")
                    self.shoot()
                    break  # 不知道为何,这里会超出索引,奇了怪.
            elif '打包绑定区' in before:
                log.info("拣货任务完成，已无商品需要拣货。")
                break
            elif '前往' in before:
                log.debug("机器人已继续移动，无推荐点可获取。")
                break
            elif '输入' in before and before[-1] == '输入':  # 有输入,就是要拣货.
                log.info("当前拣货点，仍有商品需要拣货。")
                self.picking()  # 既然还要拣货,就直接捡.
                break

    def bind_container(self, bind_info):
        # 绑定载物箱。
        self.press_ok()
        # bind_info = self.get_text()  # 直接给传
        log.debug(f"绑定载物箱流程，请给机器人绑定载物箱。载物箱信息:{bind_info}")
        if '当前作业被取消' in bind_info:
            log.debug('当前作业被取消了，注意订单，检查一下。')
            self.click_view_text('好')
            return
        tt = self.get_text()
        str_txt = ''.join(tt)  # 转成字符串

        if self.random_trigger(n=0, process='切换载具'):  # 上报异常，就不用做了。
            self.report_err('载具不合适')
            return  # 确保流程跳出去。
        if '输入' in tt:
            self.click_view_text("输入")
        if '重试' in tt:
            self.driver.tap((By.XPATH, '//*[@text="重试"]'))  # 通过元素的坐标进行点击.
        if '完成' in tt:
            self.click_view_text('完成')
        container_code = self.get_config()['container_code']
        barcode = random_string(20)
        # 获取载物箱的箱码
        try:
            container = list(interset(tt, container_code.keys()))[0]
            try:
                container_num = re.findall(r'\d/(\d)', str_txt)[0]  # 找到需要绑定的载物箱的个数.
                log.info(f"当前订单需要绑定:{container_num}个载物箱。载物箱类型：{container}")
            except:
                log.warning(f"正则获取载物箱数量出了异常，当前页面文本:{self.get_text()}")
                self.shoot()
        except IndexError:
            log.debug(f"当前需要绑定的载物箱在配置文件中没有查询到，是一个自定义的载物箱，使用万能码进行绑定。")
            container = 'x'
        if container:
            barcode = container_code.get(container, '199103181516')
        while True:
            self.press_ok()
            tmp_text = ''.join(self.get_text())
            if '扫码绑定 载物箱' in tmp_text:
                log.debug("输入载物箱码流程。")
                # self.inputcode(random_string(64))  # 1-64个长度的随机字符串.
                self.inputcode(barcode)  # 1-64个长度的随机字符串.
                sleep(1)  # 绑定单个的时候,抓太快了,会重复输一下,此时页面换了,就没有输入框了.给个延时.
                try:
                    bind_finsh_text = self.get_text()
                    log.debug(f"箱码输入完成，准备点击[完成]。结束绑定流程。当前页面文本:{bind_finsh_text}")
                    if '绑定失败' in bind_finsh_text:
                        log.warning(f"载物箱绑定失败，需要重新绑定。当前文本：{bind_finsh_text}")
                        self.inputcode(random_string(64))
                    self.click_view_text("完成", wait=2)
                    sleep(1)  # 不要等待太久,避免拣货点太近,直接到达了,错过了移动过程.
                    if '扫码绑定 载物箱' in bind_finsh_text:  # 还没绑定完
                        if '完成' not in self.get_text():  # 再次判断确定是没完成.
                            self.inputcode(random_string(64))
                        else:
                            log.warning(f"[完成]出现在当前页面，完成绑定。")
                            self.click_view_text("完成", wait=2)
                            break  # 误判,也跳出去.
                    break  # 绑定完成了
                    # container_num -= 1
                except:
                    # 这个流程,对应二次绑定时,不能再输入相同的箱码了.绑定失败后,输入框还在,这时输入一个随机码.
                    if '完成' not in self.get_text():
                        self.inputcode(random_string(64))
            elif not self.driver.element_display((By.XPATH, '//android.widget.EditText')):
                log.debug("输入框已经消失，退出输入箱码流程。")
                break  # 输入框消失了,也算完活.不要一直卡着.
            else:
                log.debug("绑定箱码流程，跳到了最后都没完成，先结束一次。")
                break

    def other_situation(self):
        # 开另一个线程来检测是否发生异常.持续检测的线程,就不要经常刷新日志了.
        view_text = self.get_text()  # 可能会空.
        view_content = self.driver.app_elements_content_desc(self.view)
        if len_same(self.get_config()['estop_text'], set(view_text)) >= 2:
            # 急停的情况.
            log.info("机器人被按下急停按钮。停止脚本。")
            exit(-104)
        elif '配置' in ''.join(view_content[:3]):  # 拉取配置界面,完成一定是靠前的
            # 获取配置的情况.
            log.info(f"云端配置改变，机器人主动拉取配置。")
            count = 5
            while count > 0:
                try:
                    # 考虑网速差,拉取的配置较大的情况.多给点时间.不过拉不完也会重新进来的,问题不大.
                    self.driver.click_element(locator=(By.XPATH, '//android.widget.Button[@content-desc="完成"]'),
                                              wait=5)
                    log.info("获取云端更新配置完成。")
                    break
                except:
                    count -= 1
                    sleep(1)

        elif '日志' in ''.join(view_content[:3]):
            # 收集日志的情况
            log.info("机器人正在收集下位机日志。")
            exit(-404)
        elif self.driver.element_display(
                locator=(By.XPATH, '//android.widget.CheckBox[contains(@text,"/sdcard/log")]')):
            log.info("机器人正在收集上位机日志。")
            exit(-404)
        elif self.driver.element_display(locator=(By.XPATH, '//*[@content-desc="设置"]')):
            log.info("GGR处在设置界面。")
            exit(-404)
        else:
            tmp_text = self.get_text(wait=10)
            if len_same(self.get_config()['sp_text'], set(tmp_text)):
                return
            else:
                log.warning("发生了一些奇怪的异常，可能需要你自己去检查一下了。")
                self.shoot()
                exit(-500)

    def get_filename(self):
        name = str(__file__).split('\\')[-1].split('.')[0]
        return name

    def api_order(self):
        site_info = read_yaml('config_file/site_info.yaml')  # {'SpeedPicker_cn1': 'sz-sqa-test''sz-sqa-test': 2}
        site = site_info[site_info[self.get_filename()]]  # 根据文本，拿到场地名称，根据场地名称，拿到场地ID。
        order_num = self.get_config()['order_num']
        try:
            res = send_order(num=order_num, siteid=site)
            if 'successData' in res:
                log.info("通过接口下发拣货任务成功。")
                sleep(20)
            else:
                log.warning("通过接口下发任务失败了，请检查一下.或者手动发单。")
                sleep(20)
        except Exception as e:
            log.warning(
                f"通过接口下发订单的流程出现了一些异常，请注意检查。异常信息:{e}\n错误行:{traceback.format_exc()}")
            sleep(10)

    def get_config(self):
        return YamlReader('speedpicker_config.yaml').data

    def shoot(self, file_name='', just_shoot=False):
        if just_shoot:  # 有些时候，不问为什么，就是要截图。
            app_screenshot(device=self.device_num()[0], file_name=file_name)
            log.debug(f"已截取机器人下位机日志。文件名称：{file_name}")
            return
            # 如何避免重复截图？1.不能通过activity去判断，持续观察发现，都是GoGoReady的，SpeedPicker流程变化，这个值不会变化。
        if self.driver.element_display((By.XPATH, '//*[contains(@content-desc,"日志上传完成")]'), wait=1) and len(
                self.shoot_text) == 0:  # 启动脚本在截图界面时，截图文本是空的，要这个做控制。
            app_screenshot(device=self.device_num()[0], file_name=file_name)
            log.debug(f"已截取机器人下位机日志。文件名称：{file_name}")
            self.shoot_text = ['截图完成']  # 占位，做判断。其他界面，会刷新
        # 最好还是看SpeedPicker当前的文本变化情况去判断是否变化了。
        elif self.sp_text and self.sp_text != self.shoot_text:  # 文本不一致了。就截图。
            # 截图
            app_screenshot(device=self.device_num()[0], file_name=file_name)
            self.shoot_text = self.sp_text  # 截图之后，刷新这次截图时的文本。 当然，有风险，要是下次还是在这个界面卡了。经验看，不会
        else:
            log.debug(f"截图流程，由于界面上的SpeedPicker文本没有产生变化，没有执行截图流程。当前文本：{self.sp_text}")

    def main(self):
        """主业务流程，通过不断的抓取页面信息。去确定当前SpeedPicker运行状态"""
        self.open_sp()
        target_location = ''
        move_flag = False
        while True:
            self.non_count = 0  # 只要在正常循环内.重置次数.
            # self.press_ok()  # 应对随时弹出来的需要协助，提示框。有必要保留,可能点掉绑定载具的"完成"
            try:
                self.sp_text = self.get_text(wait=15)  # 当前页面文本信息。  [紧急拣货中,订单ID,请放好扫码枪,完成]
                # view_content = self.driver.app_elements_text((By.XPATH, '//android.widget.TextView'))
                # log.debug(f"self.sp_text:{self.sp_text},content:{view_content}")
                ls = ''.join(self.sp_text)  # 这个是长文本。用来做一些特殊判断。
            except Exception as e:
                log.warning(f"主函数内，抓取SpeedPicker界面文本出错。跳过本次抓取。{e}")
                sleep(3)
                continue
            use_text = self.get_config()['sp_text']  # 通过配置文件读取
            set_view = set(self.sp_text)  # 去重
            if self.random_trigger(n=60):
                log.debug(f"主流程调试日志，当前文本：{self.sp_text}")  # 调试打印的，后面不用了
                # log.debug(f"主流程调试日志ls：{ls}")  # 调试打印的，后面不用了
            # elif self.islosepos():  # 丢失定位的弹窗不可定位，取消该功能。
            #     log.error("机器人丢失定位了。")
            #     break  # 跑不动了。
            elif '机器人无响应，请重试操作或重启软件' in self.sp_text:  # 这个只是文本比对，不占用时间。
                log.warning("出现机器人无响应弹窗了。")
                self.driver.tap((By.XPATH, '//*[@text="重试"]'))
            elif '关闭' in self.sp_text:  # 文本比对，不占用时间，保留。
                log.info(f"出现了[关闭]弹窗，此时的文本:{self.sp_text}")
                self.click_view_text("关闭")
            elif len(set(use_text) & set(self.sp_text)) == 0:  # 文本比对，不占用时间，保留。
                if len(self.sp_text) == 0:
                    log.debug(f"脚本抓到了空文本，跳过本次循环。")
                    sleep(1)
                    continue
                log.warning(f"页面获取的文本与SpeedPicker不符。现在拿到的是:{self.sp_text}")
                self.shoot()
                sleep(5)
                if len_same(self.get_config()['estop_text'], self.sp_text) >= 2:
                    log.warning(f"机器人已经急停，退出脚本。")
                    exit(-101)
                elif self.random_trigger(n=3, process='检查是否进入其他页面'):  # 有时候只是卡一下界面,并不需要一直检查是不是发生了异常.
                    self.other_situation()
            elif '等待任务中' in self.sp_text:  # 文本比对，不占用时间，保留。
                wait_order = 30
                log.debug(f"SpeedPicker当前没有任务，等待{wait_order}s。若仍无任务，将会通过接口下发订单。\n")
                sleep(wait_order)
                self.wait_moment("等待任务中")
            elif '前往' in self.sp_text:  # 文本比对，不占用时间，保留。
                move_flag = True
                try:
                    locate = self.sp_text[self.sp_text.index('前往') + 1]  # 前往的后一个，就是目标地点。
                except:
                    locate = ''  # 有抓错的情况.
                target_location = locate  #
                log.info(f"机器人正在前往:{locate}，请等待。")
                if locate.startswith('A0'):
                    target_info = self.get_text()
                    log.debug(f"前往目标的拣货点信息：{target_info}")
                if self.random_trigger(n=self.get_config()['pasue_psb'], process='暂停移动'):  # 触发随机。
                    self.pause_move()  # 暂停移动。
                self.wait_moment("前往")
            elif any_one(self.get_config()['bind_text'], self.sp_text) and '前往' not in self.sp_text:
                self.bind_container(self.sp_text)
            elif len_diff(self.sp_text, use_text) > 4 and re.findall('×\d+', ls):
                # 进入拣货判断逻辑：1.界面文本有非SP特征文本至少4个。2.界面文本包含至少包含2个拣货流程的特定文本。
                if not target_location.startswith('A0'):  # 移动中的目标点。
                    target_location = ''
                self.picking(picking_text=self.sp_text, target=target_location, checktarget=True,
                             ismove=move_flag)  # 封装成函数，单独处理。
                move_flag = False
            elif '已取下' in self.sp_text:  # 起脚本时,在这个界面的情况
                # 异常处理区,或者订单异常终止,都是这个流程,无需重复点.
                log.debug(f"正常取载物箱：当前任务完成，取下载物箱。")
                self.click_view_text("已取下")  # 强点.
                log.info("完成一单，不错!")
                log.debug('-·' * 30 + '-' + '\n')
                self.page_check(timeout=30, pagename='卸载载物箱', text='已取下', new_text='前往', is_shoot=True)
            elif '确定' in self.sp_text:
                log.debug(f'有确定按钮，现在点击确定。')
                self.press_ok()
                if '已取下' in self.get_text(wait=2):  # 起脚本时,在这个界面的情况
                    # 异常处理区,或者订单异常终止,都是这个流程,无需重复点.
                    log.debug(f"启动脚本时，当前任务完成，取下载物箱。")
                    self.click_view_text("已取下")  # 强点.
                    log.info("完成一单，不错!")
                    log.debug('-·' * 30 + '-' + '\n')
                # log.debug(f'调试日志，点击确定完成。')
            # elif '跳过' not in self.sp_text and (   # SpeedPicker更新，已经不展示格口信息。
            #         '拣货执行结果' in self.sp_text or interset(['格口名称', '订单编号'], self.sp_text)):  #
            #     log.debug(f"拣货结果:{self.get_text()}")
            #     # log.debug(f"拣货信息-content:{self.driver.app_elements_content_desc((By.XPATH, '//*'))}")
            #     # self.press_ok()  # 确定波次.
            #     log.debug("任务结束，确认拣货结果。")
            #     if '已取下' in self.sp_text:
            #         log.debug(f"当前任务完成，取下载物箱-2。")
            #         self.click_view_text("已取下")  # 强点.
            #         log.debug('-·' * 30 + '-' + '\n')
            #         self.wait_moment('已取下')
            #     self.click_view_text("确定")  # 强点.
            elif '安装载具' in self.sp_text:  # 文本比对，不占用时间，保留。
                log.debug("处于切换载具流程。")
                self.click_view_text("完成")
            elif len(set(self.get_config()['err_text']) & set_view) > 0:  # 异常处理区.
                log.info("当前任务上报了异常，异常信息如下:")
                log.debug(f"异常信息如下:{self.get_text()}")
                self.click_view_text("确定")  #
                self.press_ok()  # 这里可能有波次完成需要确定.再点一次,确保流程正常流转.
            elif "异常上报" in self.sp_text[:2]:  # 异常上报界面.
                log.debug("当前处于异常上报流程。")
                self.do_err()
            elif '当前作业被取消' in self.sp_text:
                log.info("当前作业被取消。")
                self.click_view_text('好')
            elif len(self.sp_text) == 1:  # 拣货执行结果,紧急拣货中,拣货中.  有可能只拿到这三个之一.
                if self.sp_text == ['speed_picker']:  # 隐藏的文本，如果抓到这个，可能只是临时的。
                    log.debug(f"当前抓取文本为空，跳过本次循环。")
                    sleep(5)  # 等待一下，跳过即可。
                else:
                    now_text = self.get_text()
                    log.warning(f"界面文本不正常的流程。之前抓到的异常文本：{self.sp_text}，现在抓到的：{now_text}")
                    if now_text != self.sp_text:
                        log.info("界面已跳转，产生了过程异常。")
                    else:
                        log.error("界面没有跳转，截图保存一下，注意查看。")
                        self.shoot()
                        sleep(5)
            elif '立即更新' in self.sp_text:
                self.click_view_text("关闭")
            elif interset(self.get_config()['manual_task'], self.sp_text):
                if self.get_config()['manual_mode']:
                    log.debug("手动派单模式，等待扫码生成任务中。")
                    self.wait_moment('开始任务')
                else:
                    log.debug("当前配置不支持手动派单模式，退出脚本，若要启动脚本，请调整配置。")
                    exit(-102)
            elif '载物箱编码：' in ls and '确定' in self.sp_text:
                log.debug(f"拣货完成，确认订单信息页面。")
                self.press_ok()  # 点了一次确认
                self.click_view_text("已取下")  # 跳到已取下界面。
                log.debug("调试日志：跳出当前页面。")
            else:
                self.press_ok()  # 这里来点一下
                sleep(5)
                now = self.get_text()
                log.warning(
                    f"main主函数里，最后一个else。为什么会走到这一步？ 刚才拿到的文本:{self.sp_text},此时的界面文本:{now}")
                if len_same(use_text, now) > 2:  # 可能只是卡了一下，重新抓一次就正常了。
                    log.debug(f"抓取到的信息正常，继续流程。")
                    if '请到此处附近' in now:
                        self.page_check(timeout=10, is_shoot=True, pagename="推荐点位检查界面", new_text='前往',
                                        new_text2='输入')  # 检查是不是半天没变化.
                else:
                    log.warning(f"抓取到的文本信息异常，请检查一下页面。")
                    self.shoot()


if __name__ == '__main__':
    while True:
        sp = SpeedPicker()
        try:
            sp.main()
            # print(sp.get_filename())
        except KeyboardInterrupt:
            log.info("手动停止脚本。")
            reset_keyboard(SpeedPicker().device_num()[0])  # 重置键盘.
        except TypeError:
            log.warning(f"抓取到的类型异常，可能是抓空了，或者界面异常了。检查一下截图。")
            # if sp.err_notify():  # 检查是否发生了一些异常。
            #     exit(-100)
            app_screenshot()  # 不管如何，截图记录一下当时的情况。
            sleep(3)  # 短暂等待一下，再继续跑。
            continue
        except Exception as e:
            timeout = 10
            log.error(
                f"发生了其他异常,{timeout}s 后将会重启脚本，异常设备："
                f"{SpeedPicker().device_num()[0]},{SpeedPicker().device_num()[1]}.注意检查:"
                f"\n1.Appium 服务起来没有。\n2.Appium端口是否正确。\n3.检查平板是否连接。\n4.检查平板是否掉线了。")
            log.warning(f"外主函数发生了异常:{e}")
            app_screenshot()
            log.info(f"报错信息:{traceback.format_exc()}")
            sleep(timeout)
