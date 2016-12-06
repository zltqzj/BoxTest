# -*- coding: utf-8 -*-
import os
import unittest
import traceback
from appium import webdriver
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.common.multi_action import MultiAction
from selenium.common.exceptions import NoSuchElementException

PATH=lambda p:os.path.abspath(os.path.join(os.path.dirname(__file__),p))

SHORT_SLEEPY_TIME = 1  #一秒钟睡眠
MIDDLE_SLEEPY_TIME = 3 #三秒钟睡眠
LOGN_SLEEPY_TIME = 5   #五秒钟睡眠

class ContactsAndroidTests(unittest.TestCase):
    #获取屏幕宽和高
    def getSize(self):
        x=self.driver.get_window_size()['width']
        y=self.driver.get_window_size()['height']
        return(x,y)

    #向左滑动
    def swipeLeft(self,t):
        l=self.getSize()
        x1=int(l[0]*0.75)
        y1=int(l[1]*0.5)
        x2=int(l[0]*0.25)
        self.driver.swipe(x1,y1,x2,y1,t)

    #屏幕向右滑动
    def swipeRight(self,t):
        l=self.getSize()
        x1=int(l[0]*0.25)
        y1=int(l[1]*0.5)
        x2=int(l[0]*0.75)
        self.driver.swipe(x1,y1,x2,y1,t)

    #向上滑动
    def swipeUp(self,t):
        l=self.getSize()
        x1=int(l[0]*0.5)
        y1=int(l[1]*0.75)
        y2=int(l[1]*0.25)
        self.driver.swipe(x1,y1,x1,y2,t)

    #向下滑动
    def swipeDown(self,t):
        l=self.getSize()
        x1=int(l[0]*0.5)
        y1=int(l[1]*0.25)
        y2=int(l[1]*0.75)
        self.driver.swipe(x1,y1,x1,y2,t)

    def setUp(self):
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '4.4.2'
        desired_caps['deviceName'] = 'Android Emulator'
        desired_caps['app'] = PATH(
            '../../../sample-code/apps/teacherbetatest-306-2.6.0-20160929.apk'
        )
        desired_caps['appPackage'] = 'com.boxfish.teacher'
        desired_caps['appActivity'] = 'com.boxfish.teacher.ui.activity.LoadingActivity'
        desired_caps["unicodeKeyboard"] = "True"
        desired_caps["resetKeyboard"] = "True"
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)


    def tearDown(self):
        print("end")


    def test_create_note(self):
        el = None
        try:
            el = self.driver.find_element_by_id("com.boxfish.teacher:id/iv_item_course_catalog_background")
            if el is None: #如果没有首页图片，说明没有登录过

                el.send_keys("zltqzj@163.com")

                el = self.driver.find_element_by_id("com.boxfish.teacher:id/ev_login_pw")
                el.send_keys("112358")

                sleep(LOGN_SLEEPY_TIME)
                el = self.driver.find_element_by_id("com.boxfish.teacher:id/btn_login")
                el.click()
        except Exception as e:
            sleep(SHORT_SLEEPY_TIME)

        #登录后
        sleep(SHORT_SLEEPY_TIME)

        #进入PASSAGE,点击PASSAGE
        el = self.driver.find_elements_by_class_name("android.widget.ImageView")

        el[1].click()
        sleep(SHORT_SLEEPY_TIME)
        #点击中级听读
        el = self.driver.find_element_by_id("com.boxfish.teacher:id/iv_item_course_grid_cell")
        el.click()
        sleep(SHORT_SLEEPY_TIME)

        #点击英雄是怎样炼成的
        el = self.driver.find_element_by_id("com.boxfish.teacher:id/sd_catalog_cover")
        el.click()
        sleep(SHORT_SLEEPY_TIME)

        #判断是否有进度条
        print('*****************+')

        el = None
        try:
            el = self.driver.find_element_by_id("com.boxfish.teacher:id/tv_download_schma")

            if el is not None:
                sleep(90)
        except Exception as e:
            sleep(SHORT_SLEEPY_TIME)



        sleep(SHORT_SLEEPY_TIME)
        #选择班级
        self.swipeLeft(1000)
        el = self.driver.find_element_by_class_name("android.widget.ListView")
        el.click()
        sleep(SHORT_SLEEPY_TIME)
        #点击下一页
        el = self.driver.find_element_by_id("com.boxfish.teacher:id/tv_next_pager")
        el.click()

        sleep(SHORT_SLEEPY_TIME)
        for i in range(10): #这段竟然没好使
            self.swipeLeft(1000)

        sleep(SHORT_SLEEPY_TIME)
        self.swipeLeft(1000)
        self.swipeLeft(1000)
        self.swipeLeft(1000)
        self.swipeLeft(1000)
        self.swipeLeft(1000)
        self.swipeLeft(1000)

        #点击activity按钮
        el = self.driver.find_element_by_id("com.boxfish.teacher:id/ib_activity")
        el.click()

        sleep(SHORT_SLEEPY_TIME)
        self.swipeLeft(1000)

        #点击朗读按钮
        el = self.driver.find_element_by_id("com.boxfish.teacher:id/rb_read")
        el.click()

        sleep(SHORT_SLEEPY_TIME)

        #朗读
        el = self.driver.find_element_by_id("com.boxfish.teacher:id/ib_record")
        el.click()

        sleep(MIDDLE_SLEEPY_TIME)
        #朗读完毕
        el = self.driver.find_element_by_id("com.boxfish.teacher:id/read_vlv")
        el.click()

        #点击背诵按钮
        el = self.driver.find_element_by_id("com.boxfish.teacher:id/rb_recite")
        el.click()
        sleep(SHORT_SLEEPY_TIME)

        el = self.driver.find_element_by_id("com.boxfish.teacher:id/ib_record")
        el.click()

        sleep(MIDDLE_SLEEPY_TIME)
        #背诵完毕
        el = self.driver.find_element_by_id("com.boxfish.teacher:id/read_vlv")
        el.click()
        sleep(SHORT_SLEEPY_TIME)


        #点击安卓返回按钮，退出朗读背诵模式
        self.driver.press_keycode(4)
        sleep(SHORT_SLEEPY_TIME)
        #翻20页课件
        for i in range(21):
            self.swipeLeft(1000)
            #sleep(SHORT_SLEEPY_TIME)

        #退出课件
        self.driver.press_keycode(4)
        sleep(SHORT_SLEEPY_TIME)

        #退出课程列表
        self.driver.press_keycode(4)
        sleep(SHORT_SLEEPY_TIME)

        #退出书籍列表
        self.driver.press_keycode(4)




if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(ContactsAndroidTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
