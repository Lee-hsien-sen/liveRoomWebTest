from page.pagebasic import PageBasic, log, Keys
import commons.page_elements as page_elements
import time
import xlrd
import os
import sys


class studentPage(PageBasic):
    '''学生页基类'''

    def __init__(self, live_id):
        PageBasic.__init__(self)
        self.get_url('http://10.200.3.125/?env=test')
        self.live_id = live_id
        self.userList = []
        self.windows = {}
        self.windows["join_windows"] = self.driver.current_window_handle
        self.classType = 0

    def getClassType(self):
        temp = self.find_element_test(page_elements.livetype.title)
        lable = temp.get_attribute('class')
        if page_elements.livetype.smallclass_live in lable:
            log.info("当前为超级小班直播课")
            self.classType = 2
        elif lable and page_elements.livetype.smallclass_live not in lable:
            log.info("当前为普通直播课")
            self.classType = 1
        else:
            log.info("页面错误")
            sys.exit(0)

    def _openStudentEndWindow(self, user_id, user_group):
        if self.driver.current_window_handle == self.windows["join_windows"]:
            self.do_click(page_elements.prejoinpage.public_class_tag)
            self.do_click("staff-3", by='name', num=1)
            self.input_text(self.live_id, "manual-tester", by='name', num=2)

        else:
            self.driver.switch_to.window(self.windows["join_windows"])
        self.input_text(user_id, "user_id", by='name')
        self.input_text(user_group, "inputGroupId", by='name')
        self.do_click(page_elements.prejoinpage.web_student_joinclass_btn)
        time.sleep(4)
        all_handles = self.driver.window_handles
        for handle in all_handles:
            if handle not in self.windows.values():
                self.driver.switch_to.window(handle)
                self.windows[user_group+'_' +
                             user_id] = self.driver.current_window_handle
                log.info(user_group+'_'+user_id+'窗口打开成功')

    def openstudentend(self, num):
        uid_exec = xlrd.open_workbook(os.getcwd() + r'\data\userList.xlsx')
        uid_sheet = uid_exec.sheet_by_index(1)
        uid_rows_num = uid_sheet.nrows
        if num > uid_rows_num:
            print('人数错误')
            return

        for index in range(num):
            user_id = str(uid_sheet.cell(index, 0).value)[:-2]
            user_group = str(uid_sheet.cell(index, 1).value)[:-2]
            self.userList.append([user_id, user_group])
        for index in self.userList:
            self._openStudentEndWindow(index[0], index[1])
        self.getClassType()
        time.sleep(5)  # 等待阿布加载


if __name__ == "__main__":
    # 5f64227c4d04ca1e49f4055b
    stu = studentPage(live_id="5f6960ad4d04ca1e49f4073b")
    num = input("请选择本次执行的学生数: ")
    num = int(num)
    stu.openstudentend(num)
    print("X"*80)
