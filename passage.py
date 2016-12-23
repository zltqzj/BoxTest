# -*- coding: utf-8 -*-
import logging
import os
import random
import time
import unittest
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')


def log(func):
    def new_func(*args, **args2):
        t0 = time.time()
        back = func(*args, **args2)
        logging.debug("%s %s --> %s [%.3fs]" % (func.__name__, args, back, time.time() - t0))
        return back

    return new_func


PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))

CATEGORY_TITLE = ''
BOOKSHELF_LEFT_SWIPE_NUMBER = 0
BOOKSHELF_UP_SWIPE_NUMBER = 0
COURSE_LIST_UP_SWIPE_NUMBER = 0
CUSTOM_CATEGORY_UP_SWIPE_NUMBER = 0

CATEGORY_NAME_BUFFER = []


class ContactsAndroidTests(unittest.TestCase):
    # 前处理
    def setUp(self):
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '6.0.1'
        desired_caps['deviceName'] = 'dd62c058'  # 'T3Q6T16310018435'  #dd62c058
        desired_caps['app'] = PATH('../../../sample-code/apps/chinese-betatest.apk')
        desired_caps['appPackage'] = 'com.boxfish.teacher'
        desired_caps['appActivity'] = 'com.boxfish.teacher.ui.activity.LoadingActivity'
        desired_caps["unicodeKeyboard"] = "True"
        desired_caps["resetKeyboard"] = "True"

        self.driver = webdriver.Remote('http://localhost:4730/wd/hub', desired_caps)
        logging.info('测试用例,Setup完成.')

    # 后处理
    def tearDown(self):
        self.driver.quit()
        logging.info('测试用例,TearDown完成.')

    # 登录系统
    # def test_login(self):
    #     try:
    #         # 清除登录信息
    #         try:
    #             el = self.driver.find_element_by_id("com.boxfish.teacher:id/iv_clear_username")
    #             el.click()
    #         except Exception as e:
    #
    #             # 填充登录信息
    #             el = self.driver.find_element_by_id("com.boxfish.teacher:id/ll_email")
    #             el.send_keys("zltqzj@163.com")
    #
    #             el = self.driver.find_element_by_id("com.boxfish.teacher:id/ev_login_pw")
    #             el.send_keys("123456")
    #
    #             el = self.driver.find_element_by_id("com.boxfish.teacher:id/btn_login")
    #             el.click()
    #
    #             # 执行判断:导航栏出现"课程"二字
    #             WebDriverWait(self.driver, 20).until(
    #                 lambda driver: self.driver.find_element_by_id('com.boxfish.teacher:id/tv_header_title').text == u'课程')
    #             print('登录成功，进入首页课程分类~')
    #
    #     except NoSuchElementException as e:
    #         logging.warn('登录操作,用户已经登录.', e)
    #
    #     except Exception as e:
    #         logging.error('登录操作,操作异常.', e)


    def test_go_category(self):
        global CATEGORY_TITLE


        # CATEGORY_TITLE = 'PASSAGE'  #测试用
        # return   #测试用

        print('进入首页')

        category_name_buffer = []
        try:
            for i in range(3):
                print('寻找导航栏标题')
                # 执行判断:导航栏出现"课程"二字
                WebDriverWait(self.driver, 20).until(
                    lambda driver: self.driver.find_element_by_id('com.boxfish.teacher:id/tv_header_title').text == u'课程')

                print('获取分类标题')
                # 获取分类标题,如TEXTBOOK,TOPIC
                el = self.driver.find_elements_by_id("com.boxfish.teacher:id/tv_item_course_catalog_name")
                category_amount = len(el)
                print('分类个数=' + str(category_amount))

                for index in range(0,category_amount):
                    category_x = el[index].size["width"] + el[index].location.get('x') + 1
                    category_y = el[index].location.get('y')
                    category_title = el[index].text
                    print('标题：' + str(category_title))
                    print('标题数组：' )
                    print  category_name_buffer

                    if category_title not in category_name_buffer:
                        category_name_buffer.append(category_title)

                        action = TouchAction(self.driver)
                        action.press(x=category_x, y=category_y).release().perform()

                        logging.info('进入第%d个类别%s操作成功'%(index,str(el[index].text)))
                        # WebDriverWait(self.driver, 10).until(
                        #     lambda driver: category_title == self.driver.find_element_by_id('com.boxfish.teacher:id/tv_header_title').text)

                        self.do_category_vertical()
                        print('-----------遍历第'+ str(index) +'个类别完毕，准备重新选择类别--------------')
                        print('-----------遍历标题：' + str(category_title) +',完毕.准备重新选择类别--------------')
                        CATEGORY_TITLE  = category_title

                        # WebDriverWait(self.driver, 10).until(
                        #     lambda driver: category_title == self.driver.find_element_by_id('com.boxfish.teacher:id/tv_header_title').text)

                        self.driver.press_keycode(4)

                print('首页上滑操作')
                self.driver.drag_and_drop(el[2], el[0])

        except Exception as e:
            print('进入分类异常')
            logging.error('进入分类异常.', e)

    #第三个测试用例，recover
    def test_go_category_recover(self):
        global  CATEGORY_TITLE
        print('恢复的title:' + str(CATEGORY_TITLE))

        if CATEGORY_TITLE == '':
            self.test_go_category()
            return

        WebDriverWait(self.driver, 20).until(
            lambda driver: driver.find_element_by_id('com.boxfish.teacher:id/tv_header_title').text == u'课程')
        print('获取分类标题')
        # 获取分类标题,如TEXTBOOK,TOPIC
        index_flag = 0
        for i  in range(3):
            print('循环第' + str(i)+'次')
            category_names = self.driver.find_elements_by_id("com.boxfish.teacher:id/tv_item_course_catalog_name")
            category_amount = len(category_names)
            print('分类个数=' + str(category_amount))

            for j in range(category_amount):
                print '----'
                print CATEGORY_TITLE
                print category_names[j].text
                print '----'
                if CATEGORY_TITLE == category_names[j].text:
                    index_flag = 1
                    break
            if index_flag == 1: #说明找到了
                for k in range(j,category_amount):
                    category_x = category_names[k].size["width"] + category_names[k].location.get('x') + 1
                    category_y = category_names[k].location.get('y')
                    category_title = category_names[k].text
                    print('标题：' + str(category_title))
                    print('标题数组：')
                    print  category_names

                    action = TouchAction(self.driver)
                    action.press(x=category_x, y=category_y).release().perform()

                    #logging.info('进入第%d个类别%s操作成功' % (i, str(print  category_name_buffer[i].text)))
                    # WebDriverWait(self.driver, 10).until(
                    #     lambda driver: category_title == self.driver.find_element_by_id('com.boxfish.teacher:id/tv_header_title').text)

                    self.do_category_vertical()
                    print('-----------遍历第' + str(k) + '个类别完毕，准备重新选择类别--------------')
                    print('-----------遍历标题：' + str(category_title) + ',完毕.准备重新选择类别--------------')
                    CATEGORY_TITLE = category_title

                    self.driver.press_keycode(4)
                break
            else:
                self.driver.drag_and_drop(category_names[2], category_names[0])

    #第四个测试用例recover2
    def test_go_category_recover2(self):
        self.test_go_category_recover()

    # 第⑤个测试用例recover3
    def test_go_category_recover3(self):
        self.test_go_category_recover()


    def do_custom_category(self):

        # 执行判断:导航栏出现"课程"二字
        WebDriverWait(self.driver, 10).until(
            lambda driver: self.driver.find_element_by_id('com.boxfish.teacher:id/iv_item_course_grid_cell'))

        grid_cell = self.driver.find_elements_by_id("com.boxfish.teacher:id/iv_item_course_grid_cell")
        grid_cell_amount = len(grid_cell)
        print('grid_cell_amount 个数 = ' + str(grid_cell_amount))

        end_flag = False
        if grid_cell_amount > 0:
            grid_cell_height = grid_cell[0].size['height']

            for index in range(0, grid_cell_amount - 2):
                grid_cell[index].click()
                self.do_course_list()
                self.driver.press_keycode(4)

            #如果cell个数小于6，无需再向上滚动
            if grid_cell_amount <= 6:
                print('cell个数小于6，无需再向上滑动')
                grid_cell[grid_cell_amount-2].click()
                self.do_course_list()
                self.driver.press_keycode(4)

                grid_cell[grid_cell_amount - 1].click()
                self.do_course_list()
                self.driver.press_keycode(4)

                return

            while True:
                print('无标题书架上滑操作')
                self.driver.drag_and_drop(grid_cell[4], grid_cell[2])

                grid_cell = self.driver.find_elements_by_id("com.boxfish.teacher:id/iv_item_course_grid_cell")
                grid_cell_amount = len(grid_cell)
                grid_cell[grid_cell_amount - 2].click()
                self.do_course_list()
                self.driver.press_keycode(4)

                grid_cell[grid_cell_amount - 1].click()
                self.do_course_list()
                self.driver.press_keycode(4)

                #无标题情况判断纵向退出的判断
                if (grid_cell_height + grid_cell[grid_cell_amount - 1].location.get('y')) == self.get_screen_size()[1]:
                    if end_flag:
                        print('------------------无标题情况纵向退出---------------------')
                        self.driver.press_keycode(4)
                        break
                    else:
                        end_flag = True
                else:
                    end_flag = False

    def do_category_vertical(self):
        try:

            # 等到iv_item_course_grid_cell出现，证明push成功
            WebDriverWait(self.driver, 10).until(
                lambda driver: self.driver.find_element_by_id('com.boxfish.teacher:id/iv_item_course_grid_cell'))

            rows_amount = len(self.driver.find_elements_by_id("com.boxfish.teacher:id/gridView")) #self.get_grid_amount()

            print('grid个数：' + str(rows_amount))

            if rows_amount == 0:
                self.do_custom_category()
                return

            for index_row in range(rows_amount):
                if rows_amount in [1, 2, 3]:
                    self.do_category_horizontal(index_row)

            if rows_amount == 3:
                # 针对退出循环条件相同的场景进行重试
                flag_retry_vertical = False

                while True:
                    print('有标题书架，上滑操作')
                    self.driver.drag_and_drop(self.get_grid()[1], self.get_grid()[0])

                    # 处理第三行
                    self.do_category_horizontal(2)

                    # 状态判断
                    if self.get_grid_amount() == 4:
                        flag_retry_vertical = False

                    elif self.get_grid_amount() == 3:
                        # 书架高度,以第二行作为标准高度
                        grid_height = self.get_grid()[1].size['height']

                        if (grid_height + self.get_grid()[2].location.get('y')) == self.get_screen_size()[1]:
                            if flag_retry_vertical:
                                print('有标题书架，结束上滑')
                                break
                            else:
                                flag_retry_vertical = True
                        else:
                            flag_retry_vertical = False
            else:
                logging.warn("课程列表出现第4行.")
        except Exception as e:
            print('纵向遍历异常')

    def do_category_horizontal(self, index):
        try:
            cells = self.get_cells(index)
            cells_amount = self.get_cells_amount(index)

            for index_column in range(cells_amount):
                if cells_amount in [1, 2, 3]:
                    cells[index_column].click()
                    self.do_course_list()
                    self.driver.press_keycode(4)

                    WebDriverWait(self.driver, 10).until(
                        lambda driver: self.driver.find_element_by_id(
                            'com.boxfish.teacher:id/tv_header_title'))

            if cells_amount == 3:
                # 针对退出循环条件相同的场景进行重试
                flag_retry_horizontal = False

                #结束的padding
                end_padding =  cells[1].location.get('x') - cells[0].location.get('x') - cells[0].size['width']
                print  'padding =' + str(end_padding)

                while True:
                    self.driver.drag_and_drop(cells[1], cells[0])
                    print('横向左滑操作')

                    # 点击第三课
                    self.get_cells(index)[2].click()
                    self.do_course_list()
                    self.driver.press_keycode(4)

                    WebDriverWait(self.driver, 10).until(
                        lambda driver: self.driver.find_element_by_id(
                            'com.boxfish.teacher:id/tv_header_title'))

                    if self.get_cells_amount(index) == 4:
                        flag_retry_horizontal = False

                    elif self.get_cells_amount(index) == 3:
                        # 书本宽度,以第二本书作为标准书宽
                        book_width = cells[1].size["width"]

                        logging.info("横向--------------书宽:" + str(book_width) + " ＋ " +
                                     "边距:" + str(cells[2].location.get('x')) + " ＝ " +
                                     "比值:" + str(book_width + cells[2].location.get('x')) + " & " +
                                     "屏宽:" + str(self.get_screen_size()[0])
                                     )

                        if (book_width + cells[2].location.get('x')) + end_padding == self.get_screen_size()[0]:
                            if flag_retry_horizontal:
                                break
                            else:
                                flag_retry_horizontal = True
                        else:
                            flag_retry_horizontal = False
            else:
                logging.warn("课程列表出现第4列.")
        except Exception as e:
            print('横向遍历异常')

    # 操作list界面
    def do_course_list(self):
        try:
            WebDriverWait(self.driver, 10).until(
                lambda driver: self.driver.find_element_by_id('com.boxfish.teacher:id/lv_book_catalog'))
            #return   #测试用,不点击list，到list界面就返回

            course_list_container = self.driver.find_element_by_id("com.boxfish.teacher:id/lv_book_catalog")
            course_item = course_list_container.find_elements_by_class_name("android.widget.LinearLayout")
            course_item_height = course_item[0].size['height']
            course_item_amount = len(course_item)

            print('list_item个数' + str(course_item_amount))


            if course_item_amount == 1:
                print('listitem个数为1的时候')
                self.go_course(course_item[0])
                pass
            elif course_item_amount == 2:
                print('listitem个数为2的时候')
                self.go_course(course_item[0])
                print('准备执行第二个')
                self.go_course(course_item[1])
                pass
            else:
                # 点击前三个，然后滚动
                print('listitem个数为3的时候')
                self.go_course(course_item[0])
                self.go_course(course_item[1])

                end_flag = False
                while True:

                    self.go_course(course_item[2])

                    self.driver.drag_and_drop(course_item[1], course_item[0])  # 上滑操作
                    print('-------list界面上滑操作--------')
                    last_course_y = course_item[course_item_amount - 1].location.get('y')
                    print('纵向------------打印list_item_height' + str(course_item_height) + '----y-' + str(
                        last_course_y) + '---screen_height' + str(self.get_screen_size()[1]))

                    if course_item_height + last_course_y == self.get_screen_size()[1]:
                        if end_flag:
                            print('----------list界面停止上滑----------')
                            break
                        else:
                            end_flag = True
                    else:
                        end_flag = False
        except Exception as e:
            print('操作list界面异常')

    def get_grid(self):
        try:
            WebDriverWait(self.driver, 10).until(
                lambda driver: self.driver.find_element_by_id('com.boxfish.teacher:id/gridView'))
            return self.driver.find_elements_by_id("com.boxfish.teacher:id/gridView")
        except Exception as e:
            print('获取grid异常')


    def get_grid_amount(self):
        return len(self.get_grid())

    def get_cells(self, index):
        try:
            grid = self.get_grid()
            print('崩溃前的index' + str(index) + '数组个数：' + str(self.get_grid_amount()))
            cells = grid[index].find_elements_by_id("com.boxfish.teacher:id/iv_item_course_grid_cell")
            return cells
        except Exception as e:
            print('获取cell异常')

    def get_cells_amount(self, index):
        return len(self.get_cells(index))

    def get_screen_size(self):
        x = self.driver.get_window_size()['width']
        y = self.driver.get_window_size()['height']
        return x, y

    def go_course(self, element):
        try:
            WebDriverWait(self.driver, 1000).until(
                lambda driver: self.driver.find_element_by_id('com.boxfish.teacher:id/tv_book_name'))

            #print('课程标题是：' + str(element.find_element_by_id('com.boxfish.teacher:id/tv_book_name').text))
            element.click()

            # 判断是否下载成功
            try:
                WebDriverWait(self.driver, 1000).until(
                    lambda driver: self.driver.find_element_by_id('com.boxfish.teacher:id/tv_listen_part_title'))
                print('下载课件成功！！！')
                self.driver.press_keycode(4)  # 测试用，到课程ppt标题页就返回
                return  #测试用，到ppt标题页就返回

            # 下载失败会出现：com.boxfish.teacher:id/confirm_button
            except Exception as e:
                print('************下载课件异常*************')
                try:
                    element.click()
                    print('点击list元素')
                    WebDriverWait(self.driver, 1000).until(
                        lambda driver: driver.find_element_by_id('com.boxfish.teacher:id/tv_listen_part_title'))

                except Exception as e:
                    confirm_button = self.driver.find_element_by_id("com.boxfish.teacher:id/confirm_button")
                    confirm_button.click()
                    element.click()
                    WebDriverWait(self.driver, 1000).until(
                        lambda driver: driver.find_element_by_id('com.boxfish.teacher:id/tv_listen_part_title'))
                    print('点击确认下载课件失败，点击list[index]，进入课件后')

            self.swipeLeft(500)
            print('左滑后选择班级')
            # 选择班级

            # 这里补救一次swipe Left
            try:
                WebDriverWait(self.driver, 10).until(
                    lambda driver: self.driver.find_element_by_id('com.boxfish.teacher:id/lv_choose_class'))
            except Exception as e:
                print('补救的左滑')
                self.swipeLeft(1000)

            choose_class = self.driver.find_element_by_id("com.boxfish.teacher:id/lv_choose_class")
            class_list = choose_class.find_elements_by_class_name("android.widget.LinearLayout")

            if len(class_list) > 0:
                random_choose = random.randint(1, len(class_list))
                class_list[random_choose - 1].click()

            # 点击下一页
            print('点击下一页')
            WebDriverWait(self.driver, 100).until(
                lambda driver: self.driver.find_element_by_id('com.boxfish.teacher:id/tv_next_pager'))
            next_page = self.driver.find_element_by_id("com.boxfish.teacher:id/tv_next_pager")
            next_page.click()

            while False == self.finish_class():
                self.swipeLeft(400)
        except Exception as e:
            print('课程ppt遍历异常')

    def finish_class(self):
        try:
            end_flag = self.driver.find_element_by_class_name("android.widget.TextView")
            if end_flag.text == 'ACHIEVEMENTS OF THIS LESSON':
                self.driver.press_keycode(4)  # 退出课件啦
                print('课件到头终止，返回list')
                return True
            else:
                return False
        except NoSuchElementException as e:
            # 可以左滑
            return False

    # 向左滑动
    def swipeLeft(self, t):
        l = self.get_screen_size()
        x1 = int(l[0] * 0.75)
        y1 = int(l[1] * 0.5)
        x2 = int(l[0] * 0.25)
        self.driver.swipe(x1, y1, x2, y1, t)

    # 屏幕向右滑动
    def swipeRight(self, t):
        l = self.get_screen_size()
        x1 = int(l[0] * 0.25)
        y1 = int(l[1] * 0.5)
        x2 = int(l[0] * 0.75)
        self.driver.swipe(x1, y1, x2, y1, t)

    # 向上滑动
    def swipeUp(self, t):
        l = self.get_screen_size()
        x1 = int(l[0] * 0.5)
        y1 = int(l[1] * 0.75)
        y2 = int(l[1] * 0.25)
        self.driver.swipe(x1, y1, x1, y2, t)

    #向下滑动
    def swipeDown(self,t):
        l=self.get_screen_size()
        x1=int(l[0]*0.5)
        y1=int(l[1]*0.25)
        y2=int(l[1]*0.75)
        self.driver.swipe(x1,y1,x1,y2,t)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(ContactsAndroidTests)
    unittest.TextTestRunner(verbosity=2).run(suite)