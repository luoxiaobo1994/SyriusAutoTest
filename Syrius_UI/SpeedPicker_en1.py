# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2021/12/9 19:17

import re
from time import sleep

from selenium.webdriver.common.by import By

from GGR import GGR
from base.common import *
from utils.log import logger


class SpeedPicker:

    def __init__(self):
        self.driver = self.init_driver()
        # sleep(10)  # 做一个长等待，没办法。加载慢。
        self.view = (By.XPATH, '//android.view.View')
        self.image = (By.XPATH, '//android.widget.ImageView')

    def device_num(self):
        num = int(__file__.split('\\')[-1].split('.')[0].split('ker')[-1]) - 1  # 序号从0开始
        devices_ls = get_devices()
        try:
            return devices_ls[num], 4725 + num * 5  # 每个设备之间，间隔5个以上
        except:
            logger.warning("There is an error in getting the UDID of the device. Please check it.")

    def init_driver(self):
        device = self.device_num()[0]  # 10.111.150.202 这种格式.
        appium_port = self.device_num()[1]
        browser = GGR().browser(devices=device, platformversion='8', port=appium_port)
        logger.info(f"Script connect Pad UDID:{device},Appium port:{appium_port}")
        return browser

    def robot_batery(self):
        tmp_text = self.driver.app_elements_content_desc()
        for i in tmp_text:
            if i.endswith('%'):
                return i
        else:
            return 'The battery level of the robot is not obtained'

    def open_sp(self):
        # 先判断是否有异常.
        if self.err_notify():  # 异常函数会自己报异常.
            exit(-404)  # 走不动了,直接停吧.
        # 抓取界面的小程序.
        desc = self.driver.app_elements_content_desc(self.view)  # if find element faile,will except,restart script
        if 'SkillSpace' not in ''.join(desc):
            logger.warning(
                "Currently not in Jrvis Launcher.")
            return
        else:
            image = self.driver.find_elements(self.image)
            soft_index = self.driver.app_elements_content_desc(self.view)
            for i in soft_index:
                if 'SpeedPicker' in i:
                    x = i.split('\n')[::-1]
                    sp_index = x.index('SpeedPicker') + 1  # 因为反过来了.从0开始.
                    self.driver.click_one(image[-sp_index])
                    logger.info("SpeedPicker not start,Auto click on SpeedPicker.")
                    sleep(2)
                    tmp_text = self.get_text()
                    for item in tmp_text:
                        if 'version:' in item:
                            logger.info(f"SpeedPicker Version:{item.split(':')[-1]}")
                            self.wait_moment(item, i=False, without="退出")
                            new_text = self.get_text()
                            if item in new_text and '退出' in new_text:
                                logger.warning(f"SpeedPicker can't start.Please check error.{new_text}")
                                exit(-404)
                    # self.wait_moment("version:") 这是部分文本.  # 'version:1.5.730'
                    break
            else:
                logger.warning(
                    f"Note: SpeedPicker is not installed on this device {self.device_num()[0]}, please install it first.")

    def err_notify(self):
        try:
            notify = self.driver.app_elements_content_desc(self.image, wait=1)  # 不用抓太久.
            if notify:
                for i in notify:
                    # The number of notifications in the upper right corner is also the image class So do a screening
                    if len(i) > 3 and '机器人' in i:
                        logger.info(
                            f"This robot [{i}] has some exceptions, please fix them first.")
                        return 1
            else:
                return 0  # Jump out of the loop and do nothing
        except:
            return 0  # Exception notification is not available at any time. Exceptions will be reported

    def inputcode(self, code='199103181516'):  # The universal code is entered by default。
        """For entering bar codes"""
        try:
            # The premise of entering numbers is to click the input button,and pop up the input box.
            # self.driver.click_element((By.XPATH, '//android.widget.EditText'))
            self.driver.input_text(locator=(By.XPATH, '//android.widget.EditText'), text=str(code))
            logger.info(f"Barcode [{code}] entered successfully.")
            self.driver.click_element((By.XPATH, '//android.widget.EditText'))  # need click input bar again
            self.driver.press_keyboard()
        except:
            pass

    def islosepos(self):
        """Determine whether the robot has lost its positioning."""
        try:
            self.driver.find_elements(
                locator=(By.XPATH, '//android.widget.ImageView[contains(@content-desc,"机器人定位丢失")]'),
                wait=1, raise_except=True)
            return 1  # return True
        except:
            sleep(0.1)

    def random_trigger(self, n=30):  # Probability value
        # Random number result, used to trigger an operation.
        if n == 0:  # Set to 0 to disable the random function.
            return 0
        elif n == 1:  # Set to 1 to keep this function on.
            return 1
        elif n >= 2:
            num = random.randint(2, n + 2)  # Start with 2 and pick a number at random
            if num == n:  # Draw this number and turn on this function
                # logger.info(A random event occurred。")
                return 1  # return True
        else:
            return 0

    def pause_move(self, time_out=25):  # 不宜过长,省得脚本卡时间,恢复按钮没了.
        """Pause movement, timeout max. 30s"""
        view_text = self.driver.app_elements_text((By.XPATH, '//android.view.View'))
        wait_time = random.randint(1, time_out)
        if '暂停' in view_text:
            self.driver.click_element((By.XPATH, '//android.view.View[@text="暂停"]'))
            logger.info(f"Click the pause button to pause the mobile robot for [{wait_time}] seconds。")
            sleep(wait_time)
            try:
                self.driver.click_element((By.XPATH, '//android.view.View[@text="恢复"]'))
                logger.info(f"The pause movement is over, and the movement will resume soon。")
                return
            except:
                logger.info("The resume button disappears. It may have been clicked manually, Exit pause move")
                return

    def press_ok(self, num=1):
        # 点击确定按钮
        count = num
        while count > 0:
            try:
                self.driver.click_element((By.XPATH, '//*[contains(@text,"确定")]'), wait=0.1)  # Not too long。
                break
            except:
                count -= 1

    def input_error(self, code):
        # Used to verify the input error barcode. The premise of execution is that the input box pops up.
        err_num = str(random.randint(0, 1000))
        self.inputcode(code=str(code) + err_num)  # Add a random number to form an error barcode.
        logger.info("A random event is triggered, and an [Error barcode] is entered.")

    def get_text(self, wait=3, raise_except=False):  # 3s左右合理,有些流程跳转时,会转圈一会儿.
        count = 20  # 有个限制.
        while count > 0:
            count -= 1  # 避免死循环
            view_ls = self.driver.app_elements_text(self.view, wait)  # 拿到异常类型的文本。文本也是view.View类型的。
            try:
                view_ls = [i for i in view_ls if i != '']  # 去重。会抓到空文本。
                if view_ls:  # 抓到才出去.在sp里,必定是会有文本页面的.
                    return view_ls
                else:
                    if count % 10 == 0:  # 偶尔刷新一次.
                        # 判断是不是在Jarvis主界面.
                        try:
                            tmp_desc = self.driver.app_elements_content_desc()
                            if 'SkillSpace' in ''.join(tmp_desc):
                                self.open_sp()
                        except:
                            pass  # The function needs to be improved
                        logger.info(
                            "The current interface does not contain documentation, if this log keeps refreshing, please check the robot.")
            except TypeError:
                if self.random_trigger(n=60):
                    logger.debug(
                        f"Random logs, don't worry, I'm continuously scraping the docs, but getting the wrong ones, see what I got:->{view_ls}<-")
                    sleep(2)
                if raise_except:
                    raise just_err
                sleep(2)
            except Exception as e:
                logger.info(f"Catch the text flow get some other exceptions:{e}")
        if count == 0:
            logger.info(f"This robot:{self.device_num()[0]}can't get text information for a long time.")
            # raise just_err  # 这个异常,并不能重启脚本.

    def get_text2(self, wait=2):
        view_ls = self.driver.app_elements_text(self.view, wait)
        if view_ls:  # 抓到才出去.在sp里,必定是会有文本页面的.
            return view_ls
        else:
            return []

    def report_err(self):
        view_ls = self.get_text()
        if view_ls[0] == '异常上报':
            logger.info("Currently, it is in the exception reporting interface.")
            self.do_err()
        else:
            try:
                self.driver.click_element((By.XPATH, '//*[@text="异常上报"]'), wait=3, raise_except=True)
                # self.click_view_text("异常上报")  # 不能这么做,点进去了,异常上报还是在文本中.
                self.do_err()
            except:
                logger.warning("The exception reporting function does not click the exception reporting button")
                return

    def do_err(self):
        # 上报异常的冗余函数.
        tmp_text = self.get_text()
        if tmp_text[0] != '异常上报':
            logger.warning(
                "Currently, it is not in the exception reporting interface, and enters the exception process by mistake")
            return
        view_ls = tmp_text[1:]
        err_type = random.choice(view_ls)
        logger.info(f"The randomly selected report type is:{err_type}")
        self.driver.click_one(self.driver.find_element((By.XPATH, '//android.view.View[@text="%s"]' % err_type)))
        count = 3
        while count > 0:
            try:
                view_ls2 = self.get_text()
                err_type2 = re.findall("确定(.*?)吗", ''.join(view_ls2))[0]
                logger.info(f"Are you sure you want to report {err_type2} exception?")
                if err_type2 == err_type or err_type == '其他':  # 确定弹窗起来了. 选择其他异常,询问框不一致.
                    self.driver.click_one(self.driver.find_elements(self.view)[-1])  # 最后一个view元素是'确定'按钮.
                    logger.info(f"Click OK to report the exception:{err_type} successfuly.")
                    if '确定' not in self.get_text():  # 跳转流程了.
                        sleep(6)  # 点完确定,会有个长等待.
                        # self.wait_moment(err_type)  # 用这个方法应该可以,需要验证一下.
                        break
                    else:
                        logger.warning("There seems to be something wrong with the exception reporting interface.")
                sleep(1)  # 暂停一下.
                count -= 1
            except:
                count -= 1
                sleep(1)
        if err_type == '载具不符':
            count = 20
            while count > 0:
                try:
                    self.click_view_text('完成', wait=3)
                    break
                except:
                    count -= 1

    def report_full(self):
        # 上报载物箱已满,前提是:Total_Picking.在拣货界面.
        view_ls = self.get_text()
        if '载物箱已满?' in view_ls:
            if self.random_trigger(n=1500):
                self.click_view_text("载物箱已满?")
                self.driver.click_one(self.driver.find_elements(self.view)[-1])
        else:
            logger.info('No cargo box is full')

    def wait_moment(self, text, timeout=1, i=True, without=None):
        # 持续去抓某个文本，直到这个文本不再这个页面了。说明流程变了。
        # 这里可能是影响效率的地方，想办法怎么优化一下。
        logger.info(f"Continuously check whether the text  [{text}] is in the current interface.")
        count = 0
        err = 10
        while err > 0:
            try:
                view_ls = self.get_text(wait=2, raise_except=True)  # 不用太频繁.
                if view_ls:  # 居然还有空的情况，干。
                    if text in view_ls:
                        if self.random_trigger(n=60):
                            if i:
                                logger.debug(f"Still check:{text},just debug log .....")
                        elif without:
                            # if without text display,break loop
                            if self.driver.element_display((By.XPATH, f'//*[@text="{without}"]')):
                                logger.debug(f"Check without text {without} display. Stop check {text}.")
                                break
                        sleep(1)  # 等待时间不能太长。
                        count += timeout  # 持续计时,看看卡界面多久了.
                        minutes = count // 60
                        if minutes >= 5:  # 每5分钟上报一次.
                            logger.warning(
                                f"The page has not changed for more than {minutes} minutes, please go to check the robot.")
                            self.err_notify()
                            break  # 出问题了，也跳出流程，等着回来吧。

                    else:
                        break  # 抓不到重复的文本了。跳出循环。
                else:
                    if self.random_trigger(n=1):
                        logger.info(f"Get None text,what's happend")
                    err -= 1  # 这种情况,也给他跳出循环.
                    sleep(timeout)
            except TypeError:
                pass  # 类型错误,前提是已经抓到元素,那么就是空文本问题,这种情况,不要跳出去.继续抓.
            except Exception as e:
                logger.warning(f"Some exceptions occurred in the process of getting text:{e}")  # 暂时先保留,现场这里问题是真的多.
                err -= 1
                sleep(1)

    def click_view_text(self, text, wait=1):
        # 强点击,保证点到.
        # logger.info(f"Ready to click：[{text}]")
        count = 3
        while count > 0:
            self.driver.click_element((By.XPATH, f'//*[@text="{text}"]'), wait=wait)
            tmp_text = self.get_text(wait=1)
            if text not in tmp_text:
                logger.info(f"Click text : [{text}] successful.")
                break
            else:
                count -= 1

    def click_input(self):
        # 用来强制点击输入的,免得有点不到的情况.
        # 不能受干扰,要是人为把这个过去了.可能就凉了.  先试试
        count = 5
        while count > 0:
            # # self.press_ok()  # 可能有弹窗干扰.
            text = self.get_text(wait=3)
            if "输入" in text:
                try:
                    self.driver.click_element((By.XPATH, '//*[@text="输入"]'))
                    if "输入" not in text:
                        logger.info("Click the enter button successfully.")
                        break
                except Exception as e:
                    count -= 1  # 不要卡流程,也给个计数限制,目前观察,最多点个两三次,肯定能点到.
                    logger.warning(f"Click input button raise exception:{e}.")
                    sleep(1)
            else:
                break  # 没有输入按钮,就不要卡流程.

    def get_total(self, view_ls):
        # 获取拣货最大数量.
        l = ''.join(view_ls)
        if '输入' in view_ls:
            for i in l.split('/'):
                if i.endswith("拣货数量"):
                    return i.split("拣货数量")[0]
        elif len({'完成', '拣货中'} & set(view_ls)) == 2:
            for i in l.split('/'):
                if "完成" in i:
                    return i.split("完成")[0]

    def find_goods(self):
        find_time = random.randint(1, 3)  # 模拟找货的时间。本身性能也一般,就不要给那么长的等待时间了.
        for i in range(find_time):
            try:
                self.driver.context  # 抓个数据，避免连接挂掉了。
            except:
                pass
            sleep(1)
        logger.info(f"wait a few seconds：{find_time}s,start picking。")

    def picking(self):
        # self.press_ok()
        view_ls = self.get_text()
        logger.info(f"The robot is currently picking goods:{view_ls}")  # 需要记录一下进入拣货流程.
        # 情况1.
        if '输入' in view_ls:  # 1.还没扫码，有输入按钮。
            # self.find_goods()  # 延时等待。不需要了.
            logger.info("Case 1, the product code has not been scanned, and the input button is about to be clicked.")
            if self.random_trigger(n=15):  # 1/15 概率，上报异常。
                self.report_err()
                return  # 结束拣货流程.
            self.click_view_text("输入")  # 点击输入按钮
            total = view_ls[-4]  # 单独的最大拣货数量。  从输入开始走,可以这么拿.
            if self.random_trigger(n=30):  # 随机触发,先去掉，100%触发。
                self.input_error(random.randint(1, 564313112131))  # 随机取一个,取对了,就可以买彩票了。

            good_code = view_ls[view_ls.index("请拣取正确货品并扫码") + 2]
            self.inputcode(code=good_code)  # 输入了商品码。
            # count = 2
            # while count < 5:
            #     # self.press_ok()  # 出现协助弹窗遮挡导致不能顺利输入问题.在载物箱流程比较严重.这里不太可能.
            #     good_code = view_ls[view_ls.index("请拣取正确货品并扫码") + count]
            #     self.inputcode(code=good_code)  # 输入了商品码。
            #     if self.driver.element_display((By.XPATH, '//android.widget.EditText')):
            #         count += 1
            #     else:
            #         # logger.info(f"确定成功输入了商品码.")
            #         break
            if total == "1":
                self.go_to()  # 一个商品,也要检查一下推荐点位.
                return  # 只捡一个，扫码完成就齐活。
            elif total != '1' and total.isdigit():
                logger.debug(f"Get max picking num:{total}")
                self.input_max(total)  # 走这个流程,到这也结束了.不需要单独的return
            else:
                logger.error(f"Get total number error,get text is {total}")  # UI变了,或者人为操作,会到这.
        # 还没扫码,但是点了输入按钮.
        elif '请拣取正确货品并扫码' in view_ls and view_ls[view_ls.index('请拣取正确货品并扫码') + 3] == '0':
            logger.info(f"Case 2, the input box pops up, but the product code is not entered.")
            tmp_text = self.get_text()
            self.inputcode(code=tmp_text[tmp_text.index('请拣取正确货品并扫码') + 2])
            self.input_total()

        elif '拣货数量' in view_ls:  # 弹出了输入商品数字的框。
            logger.info("Case 3, the product code is scanned, but the picking is not completed.")
            try:
                self.driver.find_element((By.XPATH, '//android.widget.EditText')).clear()  # 尝试一下清空.
            except:
                pass
            finally:
                # self.inputcode('9999999999')
                new_text = self.get_text()
                try:
                    num = re.findall(r'~(.*?)之间的有效数值', ''.join(new_text))[0]
                    self.inputcode(num)
                except IndexError:
                    logger.debug(f"list index out of range? {new_text}.")
                    pass  # 抓不到.退出去重来一下试试.
        else:
            # ['载物箱已满?', '拣货中', '6923450659861', '第5个商品', '1/3', '完成', '异常上报']
            logger.info("Case 4, the picking is not completed.")
            tmp_text = self.get_text()
            if '前往' in tmp_text:
                return
            logger.info(f"Scaned text:{tmp_text}")
            total = self.get_total(view_ls)  # 已经扫码的情 况下,最大值,这样处理一下.好点.
            if total == None:
                logger.info(f"Case 4,Get total number error.")
                return  # 有抓不到的情况
            logger.info(f"Scaned goods and need picking {total} goods.")
            self.input_max(total)

    def input_total(self):
        try:
            self.driver.click_element((By.XPATH, '//*[contains(@text,"/")]'), raise_except=True)  # 点击了数字框。默认点到第一个。
            tmp_text = self.get_text()
            logger.info(f"Click goods number，now page text:{tmp_text}")
            total = re.findall('1~(.*?)之间', ''.join(tmp_text))[0]
            self.inputcode(total)
            # self.press_ok()
        except:
            logger.warning("Click '/' fail,please check.")

    def input_max(self, num):
        logger.info("More than 1 product needs to be picked, click the number and enter the maximum value.")
        if self.random_trigger(n=30):  # 上报异常。
            self.report_err()
            return
        try:
            self.driver.click_element((By.XPATH, '//*[contains(@text,"/")]'), raise_except=True)  # 点击了数字框。默认点到第一个。
            logger.info(f"Click goods number，now page text:{self.get_text()}")
        except:
            logger.warning("Click '/' fail,please check.")
        self.inputcode(num)  # 输入最大数量。
        self.click_view_text("确定")  # 强行点确定.
        logger.info(f"Enter the maximum value [{num}] successfully.")
        self.go_to()

    def go_to(self):
        # 重构。
        logger.info("Picking of the current item is complete.Check where you can go.")
        count = 4
        while count > 0:
            try:
                before = self.get_text(wait=1, raise_except=True)  # 先抓一次前文本.
            except:
                continue
            if "请到此处附近" in before:
                try:
                    logger.info(f"Get a recommended target point --- {before[before.index('请到此处附近') + 1]}")
                    break
                except:
                    logger.warning(f"Out of index,why? {before}")
                    break  # 不知道为何,这里会超出索引,奇了怪.
            elif '打包绑定区' in before:
                logger.info("No items to pick, go to the packing area.")
                break
            elif '拣货中' in before and '请拣取正确货品并扫码' in before:
                logger.info("There are other items at the current location that need to be picked.")
                break
            else:
                count -= 1
                # sleep(0.5)

    def bind_carrier(self):
        # 绑定载物箱。
        logger.info("Please bind the container.")
        # self.press_ok()  # 可能超时了，先点击一下。
        if self.random_trigger(n=100):  # 上报异常，就不用做了。
            self.report_err()
            return  # 确保流程跳出去。
        if '输入' in self.get_text():
            self.click_input()
        while True:
            # self.press_ok()
            tmp_text = ''.join(self.get_text()).replace(' ', '')
            if '绑定载物箱' in tmp_text:
                self.inputcode(code=str(random.randint(1, 9999999999999)))
                sleep(1)  # 绑定单个的时候,抓太快了,会重复输一下,此时页面换了,就没有输入框了.给个延时.
                try:
                    self.click_view_text("完成")
                    break  # 绑定完成了
                except:
                    pass
            elif not self.driver.element_display((By.XPATH, '//android.widget.EditText')):
                break  # 输入框消失了,也算完活.不要一直卡着.
            else:
                break

    def other_situation(self):
        # 开另一个线程来检测是否发生异常.持续检测的线程,就不要经常刷新日志了.
        view_text = self.get_text()  # 可能会空.
        view_content = self.driver.app_elements_content_desc(self.view)
        if len({'紧急停止', '若需恢复工作', '请解除急停状态'} & set(view_text)) >= 3:
            # 急停的情况.
            logger.info("Robot is emergence stop,exit script.")
            exit(-104)
        elif '配置' in ''.join(view_content[:3]):  # 拉取配置界面,完成一定是靠前的
            # 获取配置的情况.
            logger.info(f"Webportal or GoGoInsight change some config.Wait a while to get it.")
            count = 5
            while count > 0:
                try:
                    # 考虑网速差,拉取的配置较大的情况.多给点时间.不过拉不完也会重新进来的,问题不大.
                    self.driver.click_element(locator=(By.XPATH, '//android.widget.Button[@content-desc="完成"]'), wait=5)
                    logger.info("Get config success,continue picking")
                    break
                except:
                    count -= 1
                    sleep(1)

        elif '日志' in ''.join(view_content[:3]):
            # 收集日志的情况
            logger.info("Robot is stopped,uploading log.")
            exit(-404)
        elif self.driver.element_display(
                locator=(By.XPATH, '//android.widget.CheckBox[contains(@text,"/sdcard/log")]')):
            logger.info("SpeedPicker is exit,Robot is uploading log")
            exit(-404)
        elif self.driver.element_display(locator=(By.XPATH, '//*[@content-desc="设置"]')):
            logger.info("GGR in setting page.")
            exit(-404)
        else:
            tmp_text = self.get_text(wait=10)
            if {'等待任务中', '绑定载物箱', '前往', '请扫描载物箱码或任意格口码', '已取下', '拣货异常', '拣货中', '异常上报', '输入', '暂停', '恢复'} & set(
                    tmp_text):
                # logger.info("Robot is Picking,don't worry")
                return
            else:
                logger.info("Raising some except,please check by yourself.")
                exit(-500)

    def debug_check(self):
        # 调试脚本效率的,与SP无关.
        while True:
            sleep(1)
            # try:
            print(f"{get_time()} view文本:{self.driver.app_elements_text(self.view)}")
            # except:
            #     print("?????")
            print(f"view_content:{self.driver.app_elements_content_desc(self.view)}")
            print(f"image_content:{self.driver.app_elements_content_desc(self.image)}")
            image_ico = self.driver.find_elements(self.image)
            for i in self.driver.app_elements_content_desc(self.view):
                if "SkillSpace" in i:
                    ico_name = i.split('\n')
                    self.driver.click_one(image_ico[-(len(ico_name) - ico_name.index('SpeedPicker'))])
                    print(f"{get_time()} 点击SpeedPicker")
            try:
                self.click_view_text("退出", wait=60)
                sleep(1)  #
            except:
                pass

    def main(self):
        """主业务流程，通过不断的抓取页面信息。去确定当前SpeedPicker运行状态"""
        self.open_sp()
        while True:
            self.press_ok()  # 应对随时弹出来的需要协助，提示框。
            try:
                view_ls = self.get_text(wait=15)  # 当前页面文本信息。
            except:
                continue
            ls = ''.join(view_ls)  # 这个是长文本。用来做一些特殊判断。
            use_text = {'等待任务中', '绑定载物箱', '载物箱已满?', '前往', '请扫描载物箱码或任意格口码', '已取下', '拣货异常', '拣货中', '异常上报', '输入', '暂停',
                        '恢复', '请取下载物箱 或 卸载载具上的货物', '打包'}
            if self.random_trigger(n=30):
                logger.debug(f"Randomly print log：{view_ls}")  # 调试打印的，后面不用了
            elif len(use_text & set(view_ls)) == 0:
                logger.warning(
                    f"Interface get need text fail，please check is exit SpeedPicker。\nNow Get text list:{view_ls}")
                sleep(5)
                if ['紧急停止', '若需恢复工作', '请解除急停状态'] in view_ls:
                    break
                elif self.random_trigger(3):  # 有时候只是卡一下界面,并不需要一直检查是不是发生了异常.
                    self.other_situation()
            elif '等待任务中' in view_ls:
                logger.info("Robot is waiting for task,please send orders。\n")  # 整两个空行来区分一下任务。
                self.wait_moment("等待任务中")
            elif '前往' in view_ls:
                locate = view_ls[view_ls.index('前往') + 1]  # 前往的后一个，就是目标地点。
                logger.info(f"The robot is going：{locate},please wait。")
                if self.random_trigger(n=30):  # 触发随机。
                    self.pause_move()  # 暂停移动。
                self.wait_moment("前往")
            elif '绑定载物箱' in ''.join(view_ls).replace(' ', ''):
                self.bind_carrier()
            elif len({'拣货中', '请拣取正确货品并扫码', '完成', '异常上报', '拣货数量/需拣数量', '拣货数量'} & set(view_ls)) > 2:
                # 拿到这个，说明在拣货页面。需要根据几种情况去进行处理操作。
                self.picking()  # 封装成函数，单独处理。
            elif '已取下' in ls:
                self.press_ok()  # 确定波次.
                # 异常处理区,或者订单异常终止,都是这个流程,无需重复点.
                self.click_view_text("已取下")  # 强点.
                logger.info("Finished one task,good job!")
                logger.info('~*' * 25 + '\n')
                self.wait_moment('已取下')
            elif '拣货异常' in ls:  # 异常处理区.
                logger.info("Robot in Error area，error goods list：")
                err_info = self.get_text()
                if "已取下" not in err_info:
                    for item in err_info:
                        if item != '':
                            logger.info(f"Error goods list:{item}")
            elif view_ls[0] == "异常上报":  # 异常上报界面.
                logger.info("Now in the report error interface。")
                self.do_err()
            elif self.islosepos():
                logger.error("Device lose pose。")
                break  # 跑不动了。
            else:
                pass


if __name__ == '__main__':
    while True:
        try:
            sp = SpeedPicker()
            sp.main()
            # sp.debug_check()
        except KeyboardInterrupt:
            logger.info("Stop script manual.")
            reset_keyboard(SpeedPicker().device_num()[0])  # reset keyboard
            break
        except Exception as e:
            timeout = 10
            logger.error(
                f"Other except raising,{timeout}s will restart script，Except device："
                f"{SpeedPicker().device_num()[0]},{SpeedPicker().device_num()[1]}:"
                f"\n1.Check Appium server.\n2.Check appium port.\n3.Check device udid(Pad IP).\n4.Check your devices is online")
            logger.warning(f"Raising except is:{e}")
            logger.info(f"Error line:{traceback.format_exc()}")
            sleep(timeout)
