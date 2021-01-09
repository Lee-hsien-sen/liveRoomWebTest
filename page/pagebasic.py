from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.command import Command
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from config.conf import LOCATE_MODE
from tools.times import sleep
from tools.logger import log


class PageBasic:
    """selenium基类"""

    def __init__(self):#C:\Users\admin\AppData\Local\Temp\scoped_dir12068_2047054461\Profile 1
        options= webdriver.ChromeOptions()
        options.add_argument("--use-fake-ui-for-media-stream=1")
        self.driver = webdriver.Chrome(chrome_options=options)
        self.timeout = 1
        self.wait = WebDriverWait(self.driver, self.timeout)

    def get_url(self, url):
        """打开网址并验证"""
        self.driver.maximize_window()
        self.driver.set_page_load_timeout(60)
        try:
            self.driver.get(url)
            self.driver.implicitly_wait(10)
            log.info("打开网页：%s" % url)
        except TimeoutException:
            raise TimeoutException("打开%s超时请检查网络或网址服务器" % url)


    def find_element_test(self, locator,by='xpath'):
        """寻找单个元素
           @locator 元素定位字符
           @by 定位方法可选格式 xpath/css/class/id/name
        """
        return self.wait.until(EC.presence_of_element_located((LOCATE_MODE[by],locator)))

    def find_elements_test(self, locator,by='xpath'):
        """查找多个相同的元素
           @locator 元素定位字符
           @by 定位方法可选格式 xpath/css/class/id/name
        """
        return self.wait.until(EC.presence_of_all_elements_located((LOCATE_MODE[by],locator)))

    def is_elements_exist(self,locator,by='xpath'):
        '''判断元素是否存在'''
        try:
            self.driver.find_element(by=LOCATE_MODE[by],value=locator)
            return True
        except:
            return False

    def is_elements_visibility(self, locator,by='xpath'):
        '''判断元素是否可见'''
        try:
            self.wait.until(EC.visibility_of_element_located((LOCATE_MODE[by],locator)))
            return True
        except:
            return False
    
    def elements_num(self, locator,by='xpath'):
        """获取相同元素的个数"""
        number = len(self.find_elements_test(locator,by))
        log.info("相同元素：{}".format((locator, number)))
        return number

    def input_text(self, txt, locator,by='xpath',nedclear=True,num=0):
        """输入文本
           @txt 输入文本
           @locator 元素定位字符
           @by 定位方法可选格式 xpath/css/class/id/name
           @nedclear 输入前是否需要清空
           @num 选择第几个元素进行点击
        """
        
        ele = self.find_elements_test(locator,by)[num]
        sleep()
        if nedclear:
            ele.clear()
        ele.send_keys(txt)
        log.info("输入文本：{}".format(txt))

    def do_click(self, locator,by='xpath',num=0):
        """点击
           @locator 元素定位字符
           @by 定位方法可选格式 xpath/css/class/id/name
           @num 选择第几个元素进行点击
        """
        self.find_elements_test(locator,by)[num].click()
        # wait()
        log.info("点击元素：{}".format(locator))

    def element_text(self, locator,by='xpath'):
        """获取当前元素的text"""
        
        _text = self.find_element_test(locator,by).text
        log.info("获取文本：{}".format(_text))
        return _text

    def move_by_coordinate(self,x,y,isclick=False):
        '''鼠标移动
           @x,y   绝对坐标
           @isclick 是否点击
        '''
        if isclick:
            ActionChains(self.driver).move_by_offset(x, y).click().perform()
        else:
            ActionChains(self.driver).move_by_offset(x, y).perform()


    @property
    def get_source(self):
        """获取页面源代码"""
        return self.driver.page_source

    def refresh(self):
        """刷新页面F5"""
        self.driver.refresh()
        self.driver.implicitly_wait(30)


if __name__ == "__main__":
    pass