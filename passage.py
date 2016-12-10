# -*- coding: utf-8 -*-
import os
import unittest
import traceback
import random

#from HTMLTestRunner import HTMLTestRunner
from appium import webdriver
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.common.multi_action import MultiAction
from selenium.common.exceptions import NoSuchElementException

PATH=lambda p:os.path.abspath(os.path.join(os.path.dirname(__file__),p))

debug = 1

SHORT_SLEEPY_TIME = 1  #一秒钟睡眠
MIDDLE_SLEEPY_TIME = 3 #三秒钟睡眠
LONG_SLEEPY_TIME = 5   #五秒钟睡眠


DOWNLOAD_SUCCESS = 0
HORIZONTAL_COUNT = 0
VERTICAL_COUNT = 0

width = 342
height = 456
x = 75
y = 348

class ContactsAndroidTests(unittest.TestCase):

    #配置
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

    #程序结束的地方
    def tearDown(self):
        print("end")
        #self.driver.quit()

#pragma mark - 实际测试PASSAGE的过程

    def test_passage_scan(self):

        self.isLogin() #判断是否登录

        #登录后
        sleep(SHORT_SLEEPY_TIME)

        self.chooseTemplate()  #选择一个book

        # self.judgeDownloadClass() #判断是否需要下载课件
        #
        # sleep(SHORT_SLEEPY_TIME) #睡
        #
        # self.swipeLeft(1000)  #左滑一下到选择班级界面
        #
        # sleep(MIDDLE_SLEEPY_TIME) #睡
        #
        # self.chooseClass() #选择班级
        #
        # self.scrollImagePage() #滑动课件
        #
        # self.quitBook() #退出书籍


#pragma mark - 进入课件后的操作
    def operationPpt(self):
        sleep(MIDDLE_SLEEPY_TIME) #睡

        self.swipeLeft(1000)  #左滑一下到选择班级界面
        print '左滑选择班级'
        sleep(MIDDLE_SLEEPY_TIME) #睡

        self.chooseClass() #选择班级

        self.scrollImagePage() #滑动课件



#pragma mark - 重写driver方法

    def find_element_by_id(self, eid):
        try:
            return self.driver.find_element_by_id(eid)
        except NoSuchElementException:
            return None

    def find_elements_by_id(self, eid):
        try:
            return self.driver.find_elements_by_id(eid)
        except NoSuchElementException:
            return None

    def find_element_by_class_name(self, eclass):
        try:
            return self.driver.find_element_by_class_name(eclass)
        except NoSuchElementException:
            return None

#pragma mark - 通用方法

    def transverPPT(self):
        global DOWNLOAD_SUCCESS

        cover_el = self.find_elements_by_id("com.boxfish.teacher:id/sd_catalog_cover")
        #self.driver.press_keycode(4)

        if len(cover_el) == 0:
            self.driver.press_keycode(4)
        else:
            cover_el[0].click()  #点击第一个课件
            print '下载前'
            self.judgeDownloadClass() #判断是否需要下载课件
            print '下载后'
            print DOWNLOAD_SUCCESS
            if DOWNLOAD_SUCCESS  == 1 :
                self.operationPpt() #执行完返回到课程列表
                self.driver.press_keycode(4)
                sleep(SHORT_SLEEPY_TIME)


    def tranverseBook(self):
    	#遍历书籍列表,#已进入passage
        global VERTICAL_COUNT
        global HORIZONTAL_COUNT
        for i in range(0,1):
            print '第'+ str(i) +'次遍历'
            cell_el = self.find_elements_by_id("com.boxfish.teacher:id/iv_item_course_grid_cell")
            sleep(SHORT_SLEEPY_TIME)
            print 'cell_en' + str(len(cell_el))
            if len(cell_el) == 0:
                continue

            cell_el[i].click()
            print '点击了第'+ str(i) +'本书'

            sleep(SHORT_SLEEPY_TIME)
            self.transverPPT()  #处理课件里面的内容
            self.driver.press_keycode(4)
            print '返回到格子'
            sleep(SHORT_SLEEPY_TIME)

            self.driver.swipe(width + x + x , y , x , y,1000)
            print '左滑'
            HORIZONTAL_COUNT = HORIZONTAL_COUNT + 1
            print 'HORIZONTAL_COUNT=' + str(HORIZONTAL_COUNT)
            sleep(MIDDLE_SLEEPY_TIME)
        if VERTICAL_COUNT == 2:
            self.driver.press_keycode(4)
            VERTICAL_COUNT = 0
            return
        if HORIZONTAL_COUNT == 2: #这个值为横向的个数
            #循环出来后，向上滚动1个高度
            self.driver.swipe(x,1050,x,500,1000)
            print '上滑'
            sleep(MIDDLE_SLEEPY_TIME)
            HORIZONTAL_COUNT = 0
            VERTICAL_COUNT  = VERTICAL_COUNT + 1
            print '-----------需要重置的HORIZONTAL_COUNT=' + str(HORIZONTAL_COUNT)
            self.tranverseBook()

        else:
            self.tranverseBook()


    #选择一个book,以后可改为选择某一个模板
    def chooseTemplate(self):
        global DOWNLOAD_SUCCESS
        #进入PASSAGE,点击PASSAGE
        iv_item_course_catalog_background_el = self.find_elements_by_id("com.boxfish.teacher:id/iv_item_course_catalog_background")
        print '----'
        print len(iv_item_course_catalog_background_el) #10张图

        #测试滚动
        # if len(iv_item_course_catalog_background_el) > 0 :
        #     iv_item_course_catalog_background_el[1].click() #点击passage
        #     sleep(MIDDLE_SLEEPY_TIME)
        #     #遍历书籍列表
        #     cell_el = self.find_elements_by_id("com.boxfish.teacher:id/iv_item_course_grid_cell")
        #
        #     print  "-----"
        #     self.tranverseBook()
        #测试滚动
        if len(iv_item_course_catalog_background_el) == 0:
            return

        for i in range(1,len(iv_item_course_catalog_background_el)):  #遍历类别
            print '-正在点击第'+ str(i) +'个类别'
            iv_item_course_catalog_background_el[i].click() #点击TEXTBOOK
            self.tranverseBook()

        #         cell_el = self.find_elements_by_id("com.boxfish.teacher:id/iv_item_course_grid_cell")
        #         if len(cell_el) > 0 :
        #             for j in range(0,len(cell_el)):
        #                 if cell_el[j] is not None:
        #                     cell_el[j].click() #点击书籍
        #                     print '--正在点击第' + str(j) + '本书'
        #                     cover_el = self.find_elements_by_id("com.boxfish.teacher:id/sd_catalog_cover")
        #                     if len(cover_el) > 0 :
        #                         for k in range(0,len(cover_el)):
        #                             if cover_el[k] is not None:
        #                                 cover_el[k].click()  #点击课件
        #                                 sleep(MIDDLE_SLEEPY_TIME)
        #                                 print '---正在点击第' + str(k) + '个课件'
        #                             #self.operationPpt()
        #                                 print '下载前'
        #                                 self.judgeDownloadClass() #判断是否需要下载课件
        #                                 print '下载后'
        #                             #global DOWNLOAD_SUCCESS
        #                                 print DOWNLOAD_SUCCESS
        #                                 if DOWNLOAD_SUCCESS  == 1 :
        #                                     self.operationPpt()
        #
        #                     sleep(MIDDLE_SLEEPY_TIME)  #看下位置问题
        #                     self.driver.press_keycode(4)
        #         sleep(MIDDLE_SLEEPY_TIME)
        #         self.driver.press_keycode(4)









        # if len(iv_item_course_catalog_background_el) > 0 :
        #     for i in range(0,len(iv_item_course_catalog_background_el)):
        #         print '-正在点击第'+ str(i) +'个类别'
        #         iv_item_course_catalog_background_el[i].click() #点击TEXTBOOK
        #         cell_el = self.find_elements_by_id("com.boxfish.teacher:id/iv_item_course_grid_cell")
        #         if len(cell_el) > 0 :
        #             for j in range(0,len(cell_el)):
        #                 if cell_el[j] is not None:
        #                     cell_el[j].click() #点击书籍
        #                     print '--正在点击第' + str(j) + '本书'
        #                     cover_el = self.find_elements_by_id("com.boxfish.teacher:id/sd_catalog_cover")
        #                     if len(cover_el) > 0 :
        #                         for k in range(0,len(cover_el)):
        #                             if cover_el[k] is not None:
        #                                 cover_el[k].click()  #点击课件
        #                                 sleep(MIDDLE_SLEEPY_TIME)
        #                                 print '---正在点击第' + str(k) + '个课件'
        #                             #self.operationPpt()
        #                                 print '下载前'
        #                                 self.judgeDownloadClass() #判断是否需要下载课件
        #                                 print '下载后'
        #                             #global DOWNLOAD_SUCCESS
        #                                 print DOWNLOAD_SUCCESS
        #                                 if DOWNLOAD_SUCCESS  == 1 :
        #                                     self.operationPpt()
        #
        #                     sleep(MIDDLE_SLEEPY_TIME)  #看下位置问题
        #                     self.driver.press_keycode(4)
        #         sleep(MIDDLE_SLEEPY_TIME)
        #         self.driver.press_keycode(4)


    #判断是否需要下载课件
    def judgeDownloadClass(self):
        global DOWNLOAD_SUCCESS
        DOWNLOAD_SUCCESS = 0
        #判断是否有进度条
        tv_download_schma_el = None
        try:
            print '44444'
            tv_download_schma_el = self.find_element_by_id("com.boxfish.teacher:id/tv_download_schma")
            confirm_el = self.find_element_by_id("com.boxfish.teacher:id/btn_confirm")
            if tv_download_schma_el is not None:
                print '555555'
                #有资源需要下
                driver  = self.driver
                try:
                    WebDriverWait(driver, 90).until(
                        lambda driver : driver.find_element_by_id('com.boxfish.teacher:id/tv_listen_part_title')
                    )
                    #global DOWNLOAD_SUCCESS
                    DOWNLOAD_SUCCESS = 1
                except Exception as e:
                    if confirm_el is not None:
                        confirm_el.click()
                        #callback(0)  #下载资源失败
                        print '00000000'
                        #global DOWNLOAD_SUCCESS
                        DOWNLOAD_SUCCESS = 0

                finally:
                    print '2222222'
                    sleep(LONG_SLEEPY_TIME)

                    print confirm_el.text
                    if confirm_el is not None:
                        confirm_el.click()
                        #callback(0)  #下载资源失败
                        print '00000000'
                        #global DOWNLOAD_SUCCESS
                        DOWNLOAD_SUCCESS = 0

            else:
                print '99999'
                #global DOWNLOAD_SUCCESS
                DOWNLOAD_SUCCESS = 1

            sleep(MIDDLE_SLEEPY_TIME)
            if confirm_el is not None:
                confirm_el.click()
                #global DOWNLOAD_SUCCESS
                DOWNLOAD_SUCCESS = 0
                print '888888'
                print DOWNLOAD_SUCCESS



        except Exception as e:
            sleep(SHORT_SLEEPY_TIME)

    #选择一个班级
    def chooseClass(self):
        el = self.find_element_by_class_name("android.widget.ListView")
        if el is not None:
            el.click()
            sleep(SHORT_SLEEPY_TIME)
            #点击下一页
            el = self.find_element_by_id("com.boxfish.teacher:id/tv_next_pager")
            el.click()
            sleep(SHORT_SLEEPY_TIME)
        else:
            self.driver.press_keycode(4)

    #随机左滑右滑，#随机滑动X次
    def scrollImagePage(self):

        scrollRandomCount = random.randint(15,25) #随机滑动N次
        if debug == 1:
            scrollRandomCount = random.randint(1,5)

        for i in range(1,scrollRandomCount):
            leftOrRightRandom = random.randint(1,5)
            #随机左滑右滑
            if leftOrRightRandom % 5 != 0 :
                self.swipeLeft(500)  #左滑概率大
                if debug == 0 :
                    self.readAndRecite()#读
            else:
                self.swipeRight(500) #右滑概率小
                if debug == 1 :
                    self.readAndRecite()#读

            sleep(SHORT_SLEEPY_TIME)
            #python的三目运算符和以前见的不一样啊~
            #self.swipeLeft(1000) if leftOrRightRandom % 3 != 0 else self.swipeRight(1000)


    #判断是否已登录
    def isLogin(self):
        el = None
        try:
            el = self.find_element_by_id("com.boxfish.teacher:id/iv_item_course_catalog_background")
            if el is None: #如果没有首页图片，说明没有登录过

                sleep(MIDDLE_SLEEPY_TIME)

                #清除按钮iv_clear_username
                el = self.find_element_by_id("com.boxfish.teacher:id/iv_clear_username")
                if el is not None:
                    el.click()
                el = self.find_element_by_id("com.boxfish.teacher:id/ll_email")
                el.send_keys("zltqzj@163.com")
                el = self.find_element_by_id("com.boxfish.teacher:id/ev_login_pw")

                el.send_keys("112358")
                el = self.find_element_by_id("com.boxfish.teacher:id/btn_login")
                el.click()
                sleep(LONG_SLEEPY_TIME)

        except Exception as e:
            sleep(SHORT_SLEEPY_TIME)

    #把朗读背诵单独提取出来
    def readAndRecite(self):
        #点击activity按钮
        try:
            el = self.driver.find_element_by_id("com.boxfish.teacher:id/ib_activity")
            if el is None:
                return;
        except Exception as e:
            return;
        el.click()

        sleep(SHORT_SLEEPY_TIME)
        self.swipeLeft(1000)

        #点击朗读按钮
        el = self.find_element_by_id("com.boxfish.teacher:id/rb_read")
        el.click()

        sleep(SHORT_SLEEPY_TIME)

        #朗读
        el = self.find_element_by_id("com.boxfish.teacher:id/ib_record")
        el.click()

        sleep(MIDDLE_SLEEPY_TIME)
        #朗读完毕
        el = self.find_element_by_id("com.boxfish.teacher:id/read_vlv")
        el.click()

        #点击背诵按钮
        el = self.find_element_by_id("com.boxfish.teacher:id/rb_recite")
        el.click()
        sleep(SHORT_SLEEPY_TIME)

        el = self.find_element_by_id("com.boxfish.teacher:id/ib_record")
        el.click()

        sleep(MIDDLE_SLEEPY_TIME)
        #背诵完毕
        el = self.find_element_by_id("com.boxfish.teacher:id/read_vlv")
        el.click()
        sleep(SHORT_SLEEPY_TIME)

        #点击安卓返回按钮，退出朗读背诵模式
        self.driver.press_keycode(4)
        sleep(SHORT_SLEEPY_TIME)

    #退出课件浏览
    def quitBook(self):
        #退出课件
        self.driver.press_keycode(4)
        sleep(SHORT_SLEEPY_TIME)

        #退出课程列表
        self.driver.press_keycode(4)
        sleep(SHORT_SLEEPY_TIME)

        #退出书籍列表
        self.driver.press_keycode(4)

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

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(ContactsAndroidTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
