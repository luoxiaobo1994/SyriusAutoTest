# -*- coding:utf-8 -*-
# Author: luoxiaobo
# TIME: 2021-05-05 17:37

"""
selenium的二次封装,优化第一版
"""
from time import sleep
from appium.webdriver.common.touch_action import TouchAction
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains as AC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC, select
from selenium.webdriver.support.wait import WebDriverWait as wdw
from base.common import *
from utils.log import Logger

logger = Logger().get_logger()


class TestKey:

    # 初始化关键字驱动类
    def __init__(self, driver):  # 传入一个浏览器驱动,至于是网页的还是APP都OK 不能一个动作生成一个浏览器
        logger.debug("启动脚本...")
        time.sleep(1)  # 有时候莫名其妙的卡一下,给个等待吧.
        self.driver = driver

    # 打开网页
    def open_url(self, url='https://www.baidu.com'):
        self.driver.get(url)
        logger.info(f"打开网址: {url} 成功,等待下一步操作.")

    def options(self):
        # chrome参数,不怎么用。
        options = Options()
        options.add_argument("--mute-audio")  # 静音
        options.add_experimental_option('useAutomationExtension', False)  # 取消提示参数1
        options.add_experimental_option('excludeSwitches', ['enable-automation'])  # 取消提示参数2
        return options

    # 一些属性
    @property
    def get_windows(self):
        logger.info(f"获取窗口数量成功,当前共有窗口数量为:{len(self.driver.window_handles)}")
        return self.driver.window_handles  # 当前打开的窗口数

    @property
    def get_title(self):
        logger.info(f"获取窗口标题成功,当前共有窗口标题为:{self.driver.title}")
        return self.driver.title  # 当前窗口的标题

    @property
    def page_source(self):
        logger.info(f"获取当前网页源码成功.")
        return self.driver.page_source  # 往前网页的源码

    # 最大化窗口
    def max_window(self):
        logger.info("窗口最大化.")
        self.driver.maximize_window()

    # 混合H5窗口的数量
    @property
    def context(self):
        return self.driver.contexts

    @property
    def current_centext(self):
        return self.driver.current_context

    # 获取元素的一些属性值.
    def get_attribute(self, locator, attribute='text', wait=5, i=False, raise_except=False):
        element = self.find_element(locator, wait=wait, i=i)
        try:
            return element.get_attribute(attribute)
        except:
            # self.screenshot()
            logger.error(f"元素:{locator},没有属性:{attribute}.请检查一下.")
            if raise_except:
                raise myerror

    # 定位单个元素.
    def find_element(self, locator, wait=2, i=False, raise_except=False):
        # print(locator)  # 格式是符合要求的,正确了.
        try:
            element = wdw(self.driver, wait, 0.1).until(EC.presence_of_element_located(locator))
            if i:
                logger.info(f"定位元素:{locator} 成功.")
            return element
        except:
            # logger.error(f"定位元素:{locator} 失败,注意是否有外层异常捕捉.")
            if raise_except:
                raise myerror  # 依据情况来报错。

    # 批量定位元素
    def find_elements(self, locator, wait=2, i=False, raise_except=False):
        try:
            element = wdw(self.driver, wait, 0.1).until(EC.presence_of_all_elements_located(locator))
            if i:
                logger.info(f"批量定位元素:{locator} 成功.")
            return element
        except:
            # logger.error(f"批量定位元素:{locator} 失败,注意是否有外层异常捕捉.")
            if raise_except:
                raise myerror  # 做一个返回.增加错误判断.

    # 定位并点击元素
    def click_element(self, locator, wait=1, i=False, raise_except=False):
        try:
            self.find_element(locator, wait=wait).click()
            if i:
                logger.info(f"点击元素:{locator} 成功.")
        except:
            if raise_except:
                raise myerror  # 做一个返回.增加错误判断.

    # 双击元素
    def double_click(self, locator, wait=1, i=False, raise_except=False):
        try:
            element = self.find_element(locator, wait=wait)
            AC(self.driver).double_click(element).perform()
            if i:
                logger.info(f"双击击元素:{locator} 成功.")
        except:
            self.screenshot()
            # time.sleep(0.5)  # 有时候循环抓取,避免死循环一直报错.
            logger.error(f"双击元素:{locator} 失败,请检查.")
            if raise_except:
                raise myerror  # 做一个返回.增加错误判断.

    # 元素点击,实现成功.
    def click_one(self, element, raise_except=False):
        try:
            element.click()
            # time.sleep(1)  # 点完停顿1s避免下一步操作时,页面没来得及变化.抓元素是显示等待,无所谓这个时间.
        except:
            # self.screenshot()  # 保存截图
            # time.sleep(0.5)  # 有时候循环抓取,避免死循环一直报错.
            logger.error("元素点击失败,检查一下.")
            if raise_except:
                raise myerror  # 做一个返回.增加错误判断.
            # raise myerror

    # 选择下拉框元素
    def select_value(self, locator, wait=1, value=None):
        element = self.find_element(locator, wait)
        if isinstance(value, int):
            select.Select(element).select_by_index(value)
            logger.info("按照序号选择下拉框文本成功.")
        elif isinstance(value, str):
            logger.info("按照文本选择下拉框文本成功.")
            select.Select(element).select_by_value(value)
        else:
            logger.error("下拉框选择失败.请检查输入是否正确.")

    # 判断元素是否可见,配合断言使用的.返回0 or 1,直接判断.
    def element_display(self, locator, wait=2, i=False, raise_except=False):
        try:
            element = wdw(self.driver, wait, 0.5).until(EC.presence_of_element_located(locator))
            if i:
                logger.info(f"查找元素:{locator}成功,判断通过.")
            return 1
        except:
            if raise_except:
                raise myerror  # 做一个返回.增加错误判断.

    # 判断组件数量,主要是APP端使用.配合断言使用.
    def element_num(self, locator, num=1, wait=2, i=True):
        try:
            elements = self.find_elements(locator, wait)
            if len(elements) >= num:
                if i:
                    logger.info(f"批量查找到的元素数量符合要求.判断OK")
                return 1
            else:
                logger.warning(f"批量查找到的元素数量不足.判断Fail")
                return 0
        except:
            raise myerror  # 这里不知道会不会出问题,find_elements内自带一个except.失败了不知道到得了这里不.

    # 判断组件是否存在,且文本值符合要求.
    def is_element_text(self, locator, text="", wait=2, i=True):
        try:
            count = 0
            while count < wait:
                elements = self.find_elements(locator, wait=wait)
                # print(elements)  # 正常定位
                try:
                    for ele in elements:
                        try:  # 仍有必要来一次,有些组件不含有text属性.就很烦.
                            if ele.text == text:
                                if i:  # 是否打印提示语.
                                    logger.info(f"检查页面是否含有文本:{text},通过.")
                                return 1
                            else:
                                sleep(1)
                                count += 1
                        except:
                            pass
                except:
                    logger.error(f"组件定位:{locator}失败.")
                    break
            logger.warning(f"检查页面文本:{text},失败.")
            return 0  # 返回好像有问题,调试一下.
        except:
            logger.error(f"批量定位元素:{locator}失败.")
            print(traceback.format_exc())

    # 输入文本
    def input_text(self, locator, text, wait=2):
        element = self.find_element(locator, wait)
        try:
            element.clear()  # 先进行清空.避免干扰影响
        except:
            logger.warning(f"元素输入文本:[{text}]失败.")
        finally:
            element.send_keys(text)

    # 获取元素对象的文本
    def get_element_text(self, locator, wait=2):
        return self.find_element(locator, wait).text

    # 鼠标悬停
    def move_to_element(self, locator, wait=5):
        element = self.find_element(locator, wait)
        AC(self.driver).move_to_element(element).perform()

    # 向前
    def forward(self):
        self.driver.forward()

    # 向后
    def back_forward(self):
        """ 用于网页的向前返回 """
        self.driver.back()

    def back_ui(self, n=1):
        """ 用于APP的返回上一界面 """
        for i in range(n):
            os.system("adb shell input keyevent 4")
        logger.debug("按下返回键")

    # 按下回车键
    def enter(self, locator, wait=5):
        element = self.find_element(locator, wait)
        element.send_keys(Keys.ENTER)

    # 切换窗口出
    def swtich_window(self, num=-1):
        windows = self.get_windows()
        self.driver.switch_to.window(windows[num])

    # 关闭当前窗口,窗口大于1时不会关闭浏览器
    def close(self):
        self.driver.close()  # 关闭当前的窗口
        self.driver.switch_to.window(self.get_windows()[-1])  # 跳转到当前剩余的最后一个窗口.

    # 关闭脚本
    def quit(self, time_out=5):
        for i in range(time_out):
            print(f"脚本执行完毕,{time_out - i}s后即将关闭浏览器...")
            sleep(1)
        self.driver.quit()

    # 刷新页面
    def refresh(self):
        logger.debug("刷新浏览器页面.")
        self.driver.refresh()

    # 保存截图
    def screenshot(self):
        self.driver.save_screenshot('./erro_png/%s.png' % get_time())
        logger.debug("保存截图成功.")

    # 批量按顺序打印元素文本
    def enumerate_print(self, locator, wait=5):
        logger.info("批量寻找元素,并打印文本值.")
        elements = self.find_elements(locator, wait)
        print(f"共定位到:{len(elements)}个元素.文本信息如下:")
        info = []
        # print("info:", info)
        for index, item in enumerate(elements):
            try:
                print(f"{index}.  {item.text}")
                info.append(item.text)
            except:
                pass
        return info  # 为什么返回是空的?  使用正常脚本,又是正常的

    def drag_slider(self, locator, wait=5, distance=200):
        """ 拖拽操作 """
        self.max_window()  # 滑动需要最大化窗口?
        track = self.get_track(distance)
        # print(track)
        element = self.find_element(locator, wait=wait)
        AC(self.driver).click_and_hold(element).perform()
        try:
            for x in track:
                AC(self.driver).move_by_offset(xoffset=x, yoffset=0).perform()
                # print(f"x:{x}")
                # sleep(1)
        except:
            pass
        finally:
            AC(self.driver).release().perform()  # 释放动作.

    def get_track(self, distance):
        """ 移动轨迹 """
        track = []  # 整个移动轨迹
        current = 0  # 当前位置
        mid = distance * 4 / 5  # 减速阈值
        t = 0.2  # 计算间隔
        v = 1  # 初始速度
        while current < distance:
            if current < mid:
                a = 10
            else:
                a = -30
            v0 = v  # 重新赋值初速度
            v = v0 + a * t  # 重置速度
            move = v0 * t + 1 / 2 * a * t * t  # 位移量
            current += move  # 当前位移
            track.append(round(current))
        track = set_list(track)
        return track

    # ------------------- 以下是APP方法 -------------------------------
    def wm_size(self):
        # {'width': 1080, 'height': 1920}
        logger.debug(f"获取屏幕尺寸为:{list(self.driver.get_window_size().values())[::-1]}")
        return self.driver.get_window_size()

    def swip(self, start_x, start_y, end_x, end_y, duration=1000):
        time.sleep(1)
        self.driver.swipe(start_x, start_y, end_x, end_y, duration)
        logger.debug("滑动成功.")
        sleep(0.5)  # 滑动完,APP自动化性能太差.

    def swipUp(self, duration=500):
        # 向上滑动
        wm = self.wm_size()
        self.driver.swipe(wm['width'] * 0.5, wm['height'] * 0.8, wm['width'] * 0.5, wm['height'] * 0.2, duration)
        logger.debug("向上滑动成功.")
        sleep(0.5)  # 滑动完,APP自动化性能太差.

    def swipDown(self, duration=500):
        # 向下滑动
        wm = self.wm_size()
        self.driver.swipe(wm['width'] * 0.5, wm['height'] * 0.2, wm['width'] * 0.5, wm['height'] * 0.8, duration)
        logger.debug("向下滑动成功.")
        sleep(0.5)  # 滑动完,APP自动化性能太差.

    def swipLeft(self, duration=500):
        # 向左滑动
        wm = self.wm_size()
        self.driver.swipe(wm['width'] * 0.2, wm['height'] * 0.5, wm['width'] * 0.8, wm['height'] * 0.5, duration)
        logger.debug("向左滑动成功.")
        sleep(0.5)  # 滑动完,APP自动化性能太差.

    def swipRight(self, duration=500):
        # 向右滑动
        wm = self.wm_size()
        self.driver.swipe(wm['width'] * 0.8, wm['height'] * 0.5, wm['width'] * 0.2, wm['height'] * 0.5, duration)
        logger.debug("向右滑动成功.")


    def swipto(self,dirct='up',duration=500):
        if dirct == 'up':
            x0,x1,y0,y1=0.5,0.5,0.8,0.2
        wm = self.wm_size()
        self.driver.swipe(wm['width'] * 0.8, wm['height'] * 0.5, wm['width'] * 0.2, wm['height'] * 0.5, duration)
        sleep(0.5)  # 滑动完,APP自动化性能太差.

    def tap(self, locator=None):
        size = self.find_element(locator).size
        width = size['width']
        height = size['height']
        loc = self.element_loc(locator)
        logger.debug(f"元素组件的尺寸是:{size},元素的坐标是:{loc}")
        self.driver.tap([(loc['x'] + width / 2, loc['y'] + height / 2)])  # tap([(415,1400)]),原生方法需要这么传.
        logger.debug(f"点击屏幕坐标位置: {(loc['x'], loc['y'])} 成功.如果没有后续操作,请检查是否位置坐标变化了.")
        sleep(0.5)  # 点完做一下等待,APP自动化性能太差.

    # 获取元素对象的文本
    def app_elements_text(self, locator, wait=2, i=False, d=False, raise_except=False):
        # time.sleep(1)  # 有时候会拿不到,那些APP就记得开这个等待时间.很坑.
        elements = self.find_elements(locator, wait)
        if i:
            logger.debug("获取App组件批量文本信息.")
        text = []
        if elements:
            for ele in elements:
                try:
                    if ele.text:  # 把空的干掉,空的不需要.
                        text.append(ele.text)  # 并不是所有的组件都有文本,所以,做个异常跳过.
                except:
                    pass
            if d:  # 新增参数,有时候调试需要打印一下抓到的文本信息.
                logger.debug(text)
            if raise_except:
                raise myerror
            return text
        # else:
        #     return []

    def app_elements_content_desc(self, locator, wait=2, i=False, d=False):
        elements = self.find_elements(locator, wait)
        if i:
            logger.debug("获取App组件的Content-desc文本信息.")
        content_desc = []
        for ele in elements:
            try:
                desc = ele.get_attribute("contentDescription")
                if desc:
                    content_desc.append(desc)
            except:
                pass
        return content_desc

    # APP的命令事件
    def app_command(self, num=66):
        """
        输入数值,进行操作:
        3:HOME键 4:返回键 24/25:增/减音量 187:切换应用 223:系统休眠 224:点亮屏幕
        """
        if num:
            os.system(f"adb shell input keyevent {num}")
        else:
            print("请输入正确的命令值,参考:3--HOME键 4--返回键 24/25--增/减音量 187--切换应用 223--系统休眠 224--点亮屏幕")

    # 长按事件,定位,寻找来按
    def longpress_element(self, locator, wait=5, duration=1000):
        element = self.find_element(locator, wait=wait)
        TouchAction(self.driver).long_press(el=element, duration=duration).perform()

    # 长按事件,传入已经生成的元素来按.
    def longpress_one(self, element=None, x=None, y=None, duration=1000):
        TouchAction(self.driver).long_press(el=element, x=x, y=y, duration=duration).perform()

    def element_loc(self, locator, wait=5):
        # 元素坐标 返回的是字典:x,y:{'x': 200, 'y': 1278}
        return self.find_element(locator, wait=wait).location

    def switch_context(self, num=-1):  # 默认跳转最新的那个界面.
        contexts = self.driver.contexts  # 上下文个数,类似于浏览器的几个窗口.
        self.driver.switch_to.context(contexts[num])  # 跳转目标窗口.默认最新那个.

    def press_keyboard(self, key=66, i=False):
        # 一些常用的按键编码：{回车键：66，返回键：4}  # 和adb按键重复的。干
        self.driver.press_keycode(key)
        if i:
            logger.info(f"成功按下按键:{key}，等待完成。")
        # sleep(0.5)  # 后面的函数自己有等待时间,不需要这里等了.


class myerror(Exception):
    """ 自定义的异常,用于给page层做二次异常判断的 """

    def __str__(self):
        print("报错了，没找到元素吧!!!!")


# ------------------下面是一般函数,调试用的.-----------------
def debug_1():
    driver = TestKey(webdriver.Chrome())
    driver.open_url("https://www.baidu.com")
    driver.move_to_element((By.XPATH, '//*[@id="s-usersetting-top"]'))
    sleep(1)
    driver.input_text((By.XPATH, '//input[@name="wd"]'), 'selenium')
    driver.click_element((By.XPATH, '//input[@value="百度一下"]'))
    print(driver.get_title)
    driver.enumerate_print((By.XPATH, "//h3"))
    driver.screenshot()
    driver.quit()


def debug_2(item):
    try:
        if item % 2 == 0:
            raise myerror
    except myerror:
        # print(1)
        raise myerror


def debug_3():
    try:
        debug_2(2)
    except myerror:
        print(2)


if __name__ == '__main__':
    # t = TestKey()
    # print(get_track(300))
    debug_1()
