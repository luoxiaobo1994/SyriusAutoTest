# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2021/12/9 19:17

import re
from time import sleep
from selenium.webdriver.common.by import By
from GGR import GGR
from base.common import *
from utils.log import logger
from utils.file_reader import YamlReader


class SpeedPicker:

    def __init__(self):
        self.driver = self.init_driver()
        # sleep(10)  # 做一个长等待，没办法。加载慢。
        self.view = (By.XPATH, '//android.view.View')
        self.image = (By.XPATH, '//android.widget.ImageView')
        self.notify()  # 刷新一些提醒，避免遗漏配置。
        # self.config_data = YamlReader('../config/speedpicker_config.yml')  # 准备配置话,弄好再开.
        # print(self.config_data)

    def init_driver(self):
        device = self.device_num()[0]  # 10.111.150.202 这种格式.
        appium_port = self.device_num()[1]
        # 在这里填入安卓版本,避免跑不起来.
        browser = GGR().browser(devices=device, platformversion=get_android_version(device),
                                port=appium_port)  # 自己获取安卓版本
        logger.info(f"脚本当前连接的平板:{device},安卓版本：{get_android_version(device)},Appium端口:{appium_port}")
        return browser

    def notify(self):
        """ 脚本启动的一些注意事项提醒 """
        logger.debug("注意事项：1.SpeedPicker请开启快速拣货功能。\n2.注意平板连接到此电脑。\n3.注意先启动Appium服务。")

    def device_num(self):
        num = int(__file__.split('\\')[-1].split('.')[0].split('cn')[-1]) - 1  # 序号从0开始
        devices_ls = get_devices()
        try:
            return devices_ls[num], 4725 + num * 5  # 每个设备之间，间隔5个以上
        except:
            logger.warning("获取设备UDID失败了,检查一下.")

    def robot_battery(self):
        tmp_text = self.driver.app_elements_content_desc(self.view)
        for i in tmp_text:
            if i.endswith('%') and i.split('%')[0].isdigit():
                logger.info(f"当前机器人电量为:{i}")
                return
            # logger.warning('获取机器人电池失败.')

    def open_sp(self):
        # 先判断是否有异常.
        if self.err_notify():  # 异常函数会自己报异常.
            exit(-404)  # 走不动了,直接停吧.
        # 抓取界面的小程序.
        try:
            desc = self.driver.app_elements_content_desc(self.view)  # if find element faile,will except,restart script
            if 'SkillSpace' not in ''.join(desc):
                logger.debug("当前不在Jarvis Launcher主界面.")
                return
            else:
                image = self.driver.find_elements(self.image)
                soft_index = self.driver.app_elements_content_desc(self.view)
                for i in soft_index:
                    if 'SpeedPicker' in i:
                        x = i.split('\n')[::-1]
                        sp_index = x.index('SpeedPicker') + 1  # 因为反过来了.从0开始.
                        self.driver.click_one(image[-sp_index])
                        logger.info("尚未启动SpeedPicker,即将自动启动SpeedPicker.")
                        sleep(2)
                        tmp_text = self.get_text()
                        for item in tmp_text:
                            if 'version:' in item:
                                logger.info(f"SpeedPicker的版本是:{item.split(':')[-1]}")
                                self.wait_moment(item, i=False, without="退出")
                                new_text = self.get_text()
                                if item in new_text and '退出' in new_text:
                                    logger.warning(f"发生了一些异常,SpeedPicker不能正常启动:{new_text}")
                                    exit(-404)
                        # 想办法在启动的时候,走一下更新流程.
                        if self.driver.element_display((By.XPATH, '//*[starts-with(@text,"更新")]')):
                            break
                else:
                    logger.warning(f"这个设备{self.device_num()[0]}还没有安装SpeedPicker, 请先安装.")
        except:
            return

    def update_sp(self):
        self.driver.click_element((By.XPATH, '//*[starts-with(@text,"更新")]'))  # 点击更新,应该跳转skillspace里
        self.driver.click_element((By.XPATH, '//*[@*="更新"]'))
        self.driver.click_element((By.XPATH, '//*[@*="打开"]'), wait=30)  # 下载时间有点长.

    def err_notify(self):
        try:
            notify = self.driver.app_elements_content_desc(self.image, wait=1)  # 不用抓太久.
            if notify:
                for i in notify:
                    if (len(i) > 3 and '机器人' in i) or (len(i) > 3 and '平板' in i):
                        logger.info(f"这个设备发生了一些异常:[{i}] ,请先恢复异常.")
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
            logger.info(f"条形码[{code}]输入成功.")
            self.driver.click_element((By.XPATH, '//android.widget.EditText'))  # need click input bar again
            self.driver.press_keyboard()
        except:
            pass

    def islosepos(self):
        """检查机器人是否丢失定位,但是重复了."""
        try:
            self.driver.find_elements(
                locator=(By.XPATH, '//android.widget.ImageView[contains(@content-desc,"机器人定位丢失")]'),
                wait=1, raise_except=True)
            return 1  # return True
        except:
            sleep(0.1)

    def random_trigger(self, n=30):  # Probability value
        # 获取一个随机数值，选中了，就触发随机事件。
        if n == 0:  # 设置为0，关闭随机事件。
            return 0
        elif n == 1:  # 设置为1，必中事件。
            logger.debug(f"当前所上报的异常流程,被设置为常开.注意使用.")
            return 1
        elif n >= 2:
            num = random.randint(2, n + 2)  # 1和0被排除，得多加两个。
            if num == n:  # Draw this number and turn on this function
                # logger.info(A random event occurred。")
                return 1  # return True
        else:
            return 0

    def pause_move(self, time_out=15):  # 不宜过长,省得脚本卡时间,恢复按钮没了.
        """ 暂停移动功能 """
        view_text = self.driver.app_elements_text((By.XPATH, '//android.view.View'))
        wait_time = random.randint(5, time_out)
        if '暂停' in view_text:
            self.driver.click_element((By.XPATH, '//android.view.View[@text="暂停"]'))
            logger.info(f"移动过程中,暂停移动[{wait_time}]秒钟。")
            sleep(wait_time)
            try:
                self.driver.click_element((By.XPATH, '//android.view.View[@text="恢复"]'))
                logger.info(f"暂停结束, 恢复移动。")
                return
            except:
                logger.info("恢复按钮消失了,可能是人为点击了.")
                return

    def press_ok(self, num=3, timeout=0.2):
        # logger.debug("点击确定流程.")
        # 点击确定按钮
        count = num
        while count > 0:
            try:
                self.driver.click_element((By.XPATH, '//*[@text="确定"]'), wait=timeout)
                break
            except:
                count -= 1
            # try:
            #     self.driver.click_element((By.XPATH, '//*[@text="重试"]'), wait=timeout)  # 这个不可点击.
            #     break
            # except:
            #     count -= 1
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
        logger.info("随机事件,输入一个[错误的]条码.")

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
                        logger.info("当前页面没抓到文本,如果持续刷新这个日志,请前往检查一下.")
                        self.is_other_page()  # 检查一下,是否退出了SP界面.
                        return  # 跳出去
            except TypeError:
                logger.debug("抓取文本发生类型错误异常,检查是否退出SP界面了.")
                self.is_other_page()
                if self.random_trigger(n=60):
                    logger.debug(f"随机刷日志, 脚本仍然在抓取文本中,当前可能拿到了一些不符合要求的:{view_ls}")
                    sleep(10)
                    break  # 尝试退出一下,因为总会重复刷这个日志.
                if raise_except:
                    raise just_err
                sleep(5)
            except Exception as e:
                logger.info(f"抓取文本,出现了一些别的异常:{e}")
                return  # 跳出去
        if count == 0:
            logger.info(f"这个设备:{self.device_num()[0]}有一段时间没抓到文本了,去检查一下.")
            sleep(10)  # 这里也要睡眠一下，避免刷日志太快了。
            return  # 跳出去

    def is_other_page(self):
        logger.debug("检查是否进入其他界面了.")
        try:
            if self.driver.element_display((By.XPATH, '//*[contains(content-desc,"配置信息")]')):
                logger.info("机器人正在同步配置信息,请稍后...")
                sleep(10)
            elif self.driver.element_display((By.XPATH, '//*[starts-with(@text,"/sdcard/log/")]')):
                logger.info("机器人正在收集GoGoReady日志,请稍等...")
                while True:
                    if self.driver.element_display((By.XPATH, '//*[starts-with(@text,"/sdcard/log/")]')):
                        sleep(3)
                    else:
                        break
                sleep(10)
            elif self.driver.element_display((By.XPATH, '//*[contains(@content-desc,"上传机器人日志")]')):
                logger.info("正在上传机器人日志,请稍后...")
                # self.wait_moment("上传机器人日志")
                sleep(20)
                if self.driver.element_display((By.XPATH, '//*[contains(@content-desc,"日志上传完成")]')):
                    logger.debug("机器人日志已上传完成,请自行前往解决异常,恢复机器人移动.")
                    exit(100)
            elif self.driver.element_display((By.XPATH, '//*[contains(@content-desc,"SkillSpace")]')):
                logger.info("机器人在Javis Launcher主界面,尝试重新打开SpeedPicker.")
                if self.err_notify():
                    return
                self.open_sp()
            elif self.driver.app_elements_content_desc((By.XPATH, '//*[contains(@content-desc,"完成")]')):
                self.driver.click_element((By.XPATH, '//*[contains(@content-desc,"完成")]'))
                logger.debug("同步配置完成,点击完成按钮.")
            else:
                sleep(5)
        except Exception as e:
            logger.debug(e)
            sleep(3)
        try:
            x = self.driver.app_elements_content_desc((By.XPATH, '//*'))
            logger.debug(f"x:{x}")
        except:
            logger.debug("什么都没找到")

    def report_err(self, err=''):
        view_ls = self.get_text()
        if view_ls[0] == '异常上报':
            logger.info("当前在异常上报流程.")
            self.do_err(err)
        else:
            try:
                self.driver.click_element((By.XPATH, '//*[@text="异常上报"]'), wait=3, raise_except=True)
                # self.click_view_text("异常上报")  # 不能这么做,点进去了,异常上报还是在文本中.
                self.do_err(err)
            except:
                logger.warning("异常上报流程,点击上报按钮出现了一些问题.")
                return

    def do_err(self, err=''):
        # 上报异常的冗余函数.
        tmp_text = self.get_text()
        if tmp_text[0] != '异常上报':
            logger.warning("当前在异常上报流程,但是不在异常上报界面了.去检查一下.")
            return
        if err:
            self.driver.click_one(self.driver.find_element((By.XPATH, f'//android.view.View[@text="{err}"]')))
            self.press_ok(timeout=2)  #
            return
        view_ls = tmp_text[1:]
        err_type = random.choice(view_ls)
        logger.info(f"本次随机上报的异常是:{err_type}")
        self.driver.click_one(self.driver.find_element((By.XPATH, '//android.view.View[@text="%s"]' % err_type)))
        count = 3
        while count > 0:
            try:
                view_ls2 = self.get_text()
                err_type2 = re.findall("确定(.*?)吗", ''.join(view_ls2))[0]  # 拿到的异常
                logger.info(f"确定上报[{err_type2}]异常吗?")  # 询问弹窗.
                if err_type2 == err_type or err_type == '其他':  # 确定弹窗起来了. 选择其他异常,询问框不一致.
                    self.driver.click_one(self.driver.find_elements(self.view)[-1])  # 最后一个view元素是'确定'按钮.
                    logger.info(f"确定上报:[{err_type}]异常.")
                    self.press_ok(timeout=1)  # 这里已经点击了确定，为什么还会卡呢？
                    if '确定' not in self.get_text():  # 跳转流程了.
                        sleep(6)  # 点完确定,会有个长等待.
                        # self.wait_moment(err_type)  # 用这个方法应该可以,需要验证一下.
                        break
                    else:
                        logger.warning(f"上报异常流程,好像发生了什么异常,去看看吧.此时的页面:{self.get_text()}")
                sleep(1)  # 暂停一下.
                count -= 1
            except:
                count -= 1
                sleep(1)
        if err_type == '载具不合适':
            count = 20
            while count > 0:
                try:
                    self.click_view_text('完成', wait=3)
                    logger.info("安装载具完成.")
                    break
                except:
                    count -= 1
                    sleep(1)

    def wait_moment(self, text, timeout=1, i=True, without=None):
        # 持续去抓某个文本，直到这个文本不再这个页面了。说明流程变了。
        # 这里可能是影响效率的地方，想办法怎么优化一下。
        logger.info(f"持续检查文本[{text}]是否还在当前页面.")
        count = 0
        err = 10
        while err > 0:
            try:
                view_ls = self.get_text(wait=2, raise_except=True)  # 不用太频繁.
                if view_ls:  # 居然还有空的情况，干。
                    if text in view_ls:
                        if self.random_trigger(n=60):
                            if i:
                                logger.debug(f"调试功能,持续抓取文本:[{text}]中.")
                        elif '重试' in view_ls:
                            logger.warning("出现机器人无响应弹窗了.尝试点击重试.")
                            self.driver.tap((By.XPATH, '//*[@text="重试"]'))
                        elif without:
                            # if without text display,break loop
                            if self.driver.element_display((By.XPATH, f'//*[@text="{without}"]')):
                                logger.debug(f"文本[{without}]刷新. 停止检查[{text}].")
                                break
                        sleep(1)  # 等待时间不能太长。
                        count += timeout  # 持续计时,看看卡界面多久了.
                        minutes = count // 60
                        if minutes >= 5:  # 每5分钟上报一次.
                            logger.warning(
                                f"当前页面超过{minutes}分钟没有变化了, 请检查是否发生了什么异常情况.")
                            self.err_notify()
                            break  # 出问题了，也跳出流程，等着回来吧。
                    else:
                        break  # 抓不到重复的文本了。跳出循环。
                else:
                    if self.random_trigger(n=60):
                        logger.info(f"获取到了None文本,为什么?")
                    err -= 1  # 这种情况,也给他跳出循环.
                    sleep(timeout)
            except TypeError:
                pass  # 类型错误,前提是已经抓到元素,那么就是空文本问题,这种情况,不要跳出去.继续抓.
            except Exception as e:
                logger.warning(f"持续获取的文本的流程,发生了一些异常:{e}")  # 暂时先保留,现场这里问题是真的多.
                err -= 1
                sleep(1)

    def click_view_text(self, text, wait=1, count=3):
        # 强点击,保证点到.
        while count > 0:
            self.driver.click_element((By.XPATH, f'//*[@text="{text}"]'), wait=wait)
            tmp_text = self.get_text(wait=1)
            if text not in tmp_text:
                logger.info(f"点击:[{text}]成功.")
                break
            else:
                count -= 1

    def picking(self, target=''):
        if not target.startswith('A0') and target != '':  # 在拣货点开脚本，目标点是空的。
            return  # 前往的目标点，不是货架区。说明不是拣货流程，直接跳出去。
        self.press_ok()
        view_ls = self.get_text()
        if target in view_ls:
            logger.debug(f"移动中前往的目标点位：{target},与当前到达的拣货点一致。")
        elif target and target not in view_ls:
            logger.warning(f"注意检查一下，移动中指示的目标点{target}与当前拣货页面的不一致。")
        logger.info(f"SpeedPicker处于拣货流程,页面信息:{view_ls}")  # 需要记录一下进入拣货流程.
        if '输入' in view_ls:  # 1.还没扫码，有输入按钮。
            logger.info("拣货情形1,还未扫码.")
            if self.random_trigger(n=50):  # 概率，上报异常。
                self.report_err()
                return  # 结束拣货流程.
            self.click_view_text("输入")  # 点击输入按钮
            # total = view_ls[-4]  # 单独的最大拣货数量。  从输入开始走,可以这么拿.
            if self.random_trigger(n=50):  # 随机触发,先去掉，100%触发。
                self.input_error(random.randint(1, 564313112131))  # 随机取一个,取对了,就可以买彩票了。
            try:
                good_code = view_ls[view_ls.index('×') - 1]  # 有什么办法,准确拿到商品码.
            except:
                good_code = '199103181516'
                logger.debug('没有获取到商品编码,检查一下,是不是页面排版又变化了.')
            self.inputcode(code=good_code)  # 输入了商品码。
            self.driver.click_element((By.XPATH, '//*[@text="完成"]'))
            logger.debug(f"通过点击[完成],快速完成拣货.")
        elif '异常上报' not in view_ls:
            # 拣货情形2,点开了输入框,但是没有输入商品码
            self.inputcode(code='199103181516')
            self.driver.click_element((By.XPATH, '//*[@text="完成"]'))
        else:
            # 拣货情形3,都捡完了,只是没点完成.
            self.driver.click_element((By.XPATH, '//*[@text="完成"]'))
            logger.debug(f"情形3，通过点击[完成],快速完成拣货.")
        self.go_to()

    def check_time(self):
        while True:
            temp_text = self.get_text()
            if "确定" in ''.join(temp_text):
                logger.debug(f"倒计时功能检查:{temp_text}")
            elif '重试' in temp_text:
                self.click_view_text('重试')
                break
            else:
                break

    def go_to(self):
        self.check_time()  # 放在这里检查一下,页面是否正常退出了.
        self.press_ok()  # 和倒计时功能不能共存,会主动点掉. 当然,要是倒计时点不掉,也能发现新BUG.
        logger.info("当前商品拣货完成,检查是否有推荐点.")
        count = 6
        while count > 0:
            try:
                before = self.get_text(wait=1, raise_except=True)  # 先抓一次前文本.
            except:
                continue
            if "请到此处附近" in before:
                logger.debug(f"拿到推荐点位了:{before}")
                try:
                    logger.info(f"抓取到推荐点位--->{before[before.index('请到此处附近') + 1]}")
                    break
                except:
                    logger.warning(f"抓取推荐点位,超出索引了:{before}")
                    break  # 不知道为何,这里会超出索引,奇了怪.
            elif '打包绑定区' in before:
                logger.info("拣货任务完成,已无商品需要拣货.")
                break
            elif '前往' in before:
                break
            elif '输入' in before and before[-1] == '输入':  # 有输入,就是要拣货.
                logger.info("当前拣货点,仍有商品需要拣货.")
                self.picking()  # 既然还要拣货,就直接捡.
                break
            else:
                count -= 1

    def bind_carrier(self):
        # 绑定载物箱。
        self.press_ok()
        logger.info(f"绑定载物箱流程,请给机器人绑定载物箱.载物箱信息:{self.get_text()}")
        tt = self.get_text()
        if self.random_trigger(n=0):  # 上报异常，就不用做了。
            self.report_err('载具不合适')
            return  # 确保流程跳出去。
        if '输入' in tt:
            self.click_view_text("输入")
        if '重试' in tt:
            self.driver.tap((By.XPATH, '//*[@text="重试"]'))  # 通过元素的坐标进行点击.
        if '完成' in tt:
            self.click_view_text('完成')
        while True:
            self.press_ok()
            tmp_text = ''.join(self.get_text())
            if '扫码绑定 载物箱' in tmp_text:
                logger.debug("到了输入载物箱码流程。")
                self.inputcode(random_string(64))  # 1-64个长度的随机字符串.
                # self.inputcode('Thisis6A')  # 1-64个长度的随机字符串.
                sleep(1)  # 绑定单个的时候,抓太快了,会重复输一下,此时页面换了,就没有输入框了.给个延时.
                try:
                    self.click_view_text("完成", wait=2)
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
            logger.info("机器人被按下急停按钮.停止脚本.")
            exit(-104)
        elif '配置' in ''.join(view_content[:3]):  # 拉取配置界面,完成一定是靠前的
            # 获取配置的情况.
            logger.info(f"云端配置改变,机器人主动拉取配置.")
            count = 5
            while count > 0:
                try:
                    # 考虑网速差,拉取的配置较大的情况.多给点时间.不过拉不完也会重新进来的,问题不大.
                    self.driver.click_element(locator=(By.XPATH, '//android.widget.Button[@content-desc="完成"]'), wait=5)
                    logger.info("获取云端更新配置完成.")
                    break
                except:
                    count -= 1
                    sleep(1)

        elif '日志' in ''.join(view_content[:3]):
            # 收集日志的情况
            logger.info("机器人正在收集下位机日志.")
            exit(-404)
        elif self.driver.element_display(
                locator=(By.XPATH, '//android.widget.CheckBox[contains(@text,"/sdcard/log")]')):
            logger.info("机器人正在收集上位机日志")
            exit(-404)
        elif self.driver.element_display(locator=(By.XPATH, '//*[@content-desc="设置"]')):
            logger.info("GGR处在设置界面.")
            exit(-404)
        else:
            tmp_text = self.get_text(wait=10)
            if {'等待任务中', '绑定载物箱', '前往', '请扫描载物箱码或任意格口码', '已取下', '拣货异常', '拣货中', '异常上报', '输入', '暂停', '恢复'} & set(
                    tmp_text):
                return
            else:
                logger.info("发生了一些奇怪的异常,可能需要你自己去检查一下了.")
                exit(-500)

    def main(self):
        """主业务流程，通过不断的抓取页面信息。去确定当前SpeedPicker运行状态"""
        self.open_sp()
        target_location = ''
        while True:
            self.press_ok()  # 应对随时弹出来的需要协助，提示框。有必要保留,可能点掉绑定载具的"完成"
            try:
                view_ls = self.get_text(wait=15)  # 当前页面文本信息。
                # logger.debug(f"view_ls:{view_ls}")
                ls = ''.join(view_ls)  # 这个是长文本。用来做一些特殊判断。
            except:
                continue
            use_text = {'等待任务中', '紧急拣货中', '前往', '拣货异常', '拣货中', '异常上报', '输入', '暂停', '恢复',
                        '拣货执行结果', '隔口名称', '任务被终止', '请取下载物箱或货品', '已取下'}
            set_view = set(view_ls)
            if self.random_trigger(n=60):
                logger.debug(f"主流程调试日志：{view_ls}")  # 调试打印的，后面不用了
            elif '机器人无响应，请重试操作或重启软件' in view_ls:
                logger.warning("出现机器人无响应弹窗了.")
                self.driver.tap((By.XPATH, '//*[@text="重试"]'))
            elif '关闭' in view_ls:
                self.click_view_text("关闭")
            elif len(use_text & set(view_ls)) == 0:
                logger.warning(f"页面获取的文本与SP不符。\n现在拿到的是:{view_ls}")
                sleep(5)
                if ['紧急停止', '若需恢复工作', '请解除急停状态'] in view_ls:
                    break
                elif self.random_trigger(3):  # 有时候只是卡一下界面,并不需要一直检查是不是发生了异常.
                    self.other_situation()
            elif '等待任务中' in view_ls:
                logger.info("SpeedPicker当前没有任务,请下单。\n")  # 整两个空行来区分一下任务。
                self.wait_moment("等待任务中")
            elif '前往' in view_ls:
                locate = view_ls[view_ls.index('前往') + 1]  # 前往的后一个，就是目标地点。
                target_location = locate
                logger.info(f"机器人正在前往:{locate},请等待。")
                if locate.startswith('A0'):
                    logger.debug(f"前往目标的拣货点信息：{self.get_text()}")
                if self.random_trigger(n=2):  # 触发随机。
                    self.pause_move()  # 暂停移动。
                self.wait_moment("前往")
            elif any_one(['扫码绑定 载物箱', '扫码绑定载物箱', '请放置好载物箱，并归位扫码枪'], view_ls):
                self.bind_carrier()
            elif len(set_view.difference(use_text)) >= 4 and '拣货中' in ls:  # 储位,商品名称/编码,数量,x
                # 拿到这个，说明在拣货页面。需要根据几种情况去进行处理操作。
                self.picking(target=target_location)  # 封装成函数，单独处理。
            elif ['格口名称', '单据'] in view_ls:  # 被改掉了.
                logger.debug(f"拣货结果:{self.get_text()}")
                self.press_ok()
                # 异常处理区,或者订单异常终止,都是这个流程,无需重复点.
                self.click_view_text("已取下")  # 强点.
                logger.info("完成一单,不错!")
                logger.info('~*' * 25 + '\n')
                self.wait_moment('已取下')
            elif '已取下' in view_ls or '拣货执行结果' in view_ls:
                # logger.debug(f"拣货信息-text:{self.get_text()}")
                # logger.debug(f"拣货信息-content:{self.driver.app_elements_content_desc((By.XPATH,'//*'))}")
                self.press_ok()  # 确定波次.
                # 异常处理区,或者订单异常终止,都是这个流程,无需重复点.
                self.click_view_text("已取下")  # 强点.
                logger.info("完成一单,不错!")
                logger.info('~*' * 25 + '\n')
                self.wait_moment('已取下')
            elif '安装载具' in view_ls:
                self.click_view_text("完成")
            elif '拣货异常' in ls:  # 异常处理区.
                logger.info("当前任务上报了异常,异常信息如下:")
                err_info = self.get_text()  # 可以根据'编码:'去拿到有几个异常商品.
                err_goods_ls = []
                for item in err_info:  # 先拿到有几个异常订单.
                    if item.startswith('编码'):
                        err_goods_ls.append(item)
                for goods in err_goods_ls:
                    logger.info(
                        f"商品码:{goods.split('编码')[-1]},"
                        f"名称:{err_info[err_info.index(goods) - 1]},"
                        f"商品储位:{err_info[err_info.index(goods) - 3]},"
                        f"{err_info[err_info.index(goods) - 4]},"  # 订单
                        f"商品异常:{err_info[err_info.index(goods) - 5]}"
                    )
                self.click_view_text("确定")  #
                self.press_ok()  # 这里可能有波次完成需要确定.
            elif view_ls[0] == "异常上报":  # 异常上报界面.
                logger.info("当前处于异常上报流程。")
                self.do_err()
            elif self.islosepos():
                logger.error("机器人丢失定位了。")
                break  # 跑不动了。
            elif '当前作业被取消' in view_ls:
                self.click_view_text('好')
            elif len(view_ls) == 1:  # 拣货执行结果,紧急拣货中,拣货中.  有可能只拿到这三个之一.
                sleep(1)
            else:
                self.press_ok()  # 这里来点一下
                logger.debug(f"main主函数里,最后一个else.为什么会走到这一步? 刚才拿到的文本:{view_ls},此时的界面文本:{self.get_text()}")
                self.robot_battery()


if __name__ == '__main__':
    while True:
        try:
            sp = SpeedPicker()
            sp.main()
        except KeyboardInterrupt:
            logger.info("手动停止脚本.")
            reset_keyboard(SpeedPicker().device_num()[0])  # 重置键盘.
        except Exception as e:
            timeout = 10
            logger.error(
                f"发生了其他异常,{timeout}s 后将会重启脚本,异常设备："
                f"{SpeedPicker().device_num()[0]},{SpeedPicker().device_num()[1]}.注意检查:"
                f"\n1.Appium 服务起来没有.\n2.Appium端口是否正确.\n3.检查平板是否连接.\n4.检查平板是否掉线了.")
            logger.warning(f"发生了异常:{e}")
            logger.info(f"报错信息:{traceback.format_exc()}")
            sleep(timeout)
