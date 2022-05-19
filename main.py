import sys

import numpy as np
from PyQt5 import QtCore,QtGui,QtWidgets
from PyQt5.QtWidgets import *
from MainWindow import Ui_MainWindow
from PyQt5.QtCore import QUrl
from PyQt5.QtSql import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
from six.moves import urllib
import matplotlib
matplotlib.use("Qt5Agg")  # 声明使用QT5
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import os
import sys
# captcha是用于生成验证码图片的库，可以 pip install captcha 来安装它
from captcha.image import ImageCaptcha
import sys

from win32com.client import Dispatch
import random
matplotlib.rcParams['font.sans-serif'] = ['SimHei']  #设置中文字体
matplotlib.rcParams['axes.unicode_minus'] = False

current = ['0','0','0','0','0','0','0','0','0','0','0','0','0','0']
id = 0
b_id = []
eb_id = []
pb_id = []
booktype =''
url = ''
code = ''
verify=''
path = ''

class QSSLoader:
    def __init__(self):
        pass

    @staticmethod
    def read_qss_file(qss_file_name):
        with open(qss_file_name, 'r',  encoding='UTF-8') as file:
            return file.read()


class MyFigure(FigureCanvas):
    def __init__(self,width, height, dpi):
        self.fig = Figure(figsize=(width, height), dpi=dpi) # 创建一个Figure
        super(MyFigure,self).__init__(self.fig) # 在父类中激活Figure窗口
        self.axes = self.fig.add_subplot(111)# 调用Figure下面的add_subplot方法

def random_captcha_text(num):
    # 验证码列表
    captcha_text = []
    for i in range(10):  # 0-9数字
        captcha_text.append(str(i))
    for i in range(65, 91):  # 对应从“A”到“Z”的ASCII码
        captcha_text.append(chr(i))
    for i in range(97, 123):  # 对应从“a”到“z”的ASCII码
        captcha_text.append(chr(i))

    # 从list中随机获取6个元素，作为一个片断返回
    example = random.sample(captcha_text, num)

    # 将列表里的片段变为字符串并返回
    verification_code = ''.join(example)
    return verification_code


# 生成字符对应的验证码
def generate_captcha_image():
    global verify
    global path
    image = ImageCaptcha()
    # 获得随机生成的验证码
    captcha_text = random_captcha_text(4)
    # 把验证码列表转为字符串
    captcha_text = ''.join(captcha_text)
    verify = captcha_text
    # 生成验证码
    path = os.path.abspath('main.py')
    path = path[:-7]+'code\\'
    print(path)
    if not os.path.exists(path):
        print("目录不存在!,已自动创建")
        os.makedirs(path)
    print("生成的验证码的图片为：", captcha_text)
    image.write(captcha_text, path + captcha_text + '.png')

class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.stackedWidget.setCurrentIndex(2)
        self.tutorstack.setCurrentIndex(1)
        self.Le_vx.hide()#联系更新框隐藏
        self.Le_name.hide()
        self.btn_vxfinish.hide()
        self.btn_namefinish.hide()
        self.showData.setSelectionBehavior(QAbstractItemView.SelectRows)#选中全行
        self.mytable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.showData.setEditTriggers(QAbstractItemView.NoEditTriggers)#禁止编辑
        self.lab_warn.hide()#密码不一致
        self.logwarn.hide()#登录失败警告
        self.uurl.show()
        self.luurl.show()
        self.uplatform.show()
        self.luplatform.show()
        self.uu_type.show()
        self.comu_type.show()
        self.ucode.show()
        self.lucode.show()
        self.ueb_type.show()
        self.comeb_type.show()
        self.uprice.hide()
        self.luprice.hide()
        self.ucondi.hide()
        self.comcondi.hide()
        self.combo_condition.hide()
        self.rlogpwd.setEchoMode(QLineEdit.Password)
        self.logpwd.setEchoMode(QLineEdit.Password)
        self.logrpwd.setEchoMode(QLineEdit.Password)
        self.labprice.hide()
        self.lab_price.hide()
        self.lucode.hide()
        self.ucode.hide()
        self.btn_out.hide()
        generate_captcha_image()
        global verify
        global path
        path = path + verify + '.png'
        print(path)
        jpg = QtGui.QPixmap(r'%s' % (path)).scaled(self.label.width(), self.label.height())
        self.vertification.setPixmap(jpg)



    #数据库连接
    db = QSqlDatabase.addDatabase("QODBC")
    db.setDatabaseName("Driver={Sql Server};Server=localhost;Database=master;Uid=sa;Pwd=123456")
    if(db.open()):
        print("数据库连接成功")
    db.open()
    query = QSqlQuery()
    query.exec("Use BookShare")
    query.exec("go")


    #关闭函数
    def Btn_exit(self):
        mainWindow.close()
    def Btn_about_us(self):
        mesBox = QMessageBox()
        mesBox.setWindowTitle('开发者信息')
        mesBox.setText('2020STAT DB GROUP\nVersion:beta 0.0.1\nBased on PyQt5\nFor more \non Github:https://github.com/Tobedust')
        mesBox.setIcon(QMessageBox.Information)
        mesBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        mesBox.setStyleSheet("QPushButton:hover{background-color: rgb(216, 227, 255);}")
        mesBox.exec_()

    def Btn_ebook(self):
        #跳转页面
        self.stackedWidget.setCurrentIndex(3)

        #数据框展示
        self.model = QSqlTableModel()
        self.showData.setModel(self.model)
        # self.model.setEditStrategy(QSqlTableModel.OnFieldChange)  # 允许字段更改
        #self.model.select()  # 查询所有数据
        query1 = "select * from EBOOK1"
        query = QSqlQuery(query1)
        self.model.setQuery(query)
        self.model.query()

    def Btn_detail(self):
        global url
        global code
        # index = self.showData.currentIndex()
        row = self.showData.currentIndex().row()
        if(row ==-1):
            mesBox = QMessageBox()
            mesBox.setWindowTitle('提示')
            mesBox.setText(
                '请选择你所需要的行')
            mesBox.setIcon(QMessageBox.Information)
            mesBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            mesBox.setStyleSheet("QPushButton:hover{background-color: rgb(216, 227, 255);}")
            mesBox.exec_()
        else:
            for i in range(14):
                index = self.model.index(row, i)
                # self.model.removeRow(index.row())
                current[i] = self.model.data(index)
                # current.append(a)
            print(current)
            url = current[8]
            code = current[10]
            print(url)
            print(code)
            self.stackedWidget.setCurrentIndex(1)
            self.lab_title.setText(current[1])
            self.lab_author.setText(current[2])
            self.lab_edition.setText(current[3])
            self.lab_publisher.setText(current[4])
            self.lab_etype.setText(current[7])
            self.lab_rating.setText(str(current[12]))
            self.lab_dnld_2.setText(str(current[13]))
            self.lab_price.setText(str(current[6]))
            if booktype == "实体书":
                self.labetype.hide()
                self.lab_etype.hide()
                self.labrating.hide()
                self.lab_rating.hide()
                self.labdnld.hide()
                self.lab_dnld_2.hide()
                self.labprice.show()
                self.lab_price.show()
            if current[10] == "直链":
                self.btn_url.hide()
                self.lab_url.hide()
                self.btn_thunder.show()
                self.lab_thunder.show()
            else:
                self.btn_thunder.hide()
                self.lab_thunder.hide()
                self.btn_url.show()
                self.lab_url.show()

    def Btn_rating(self):
        rate = self.ratingslider.value()/100
        print(rate)
        query = QSqlQuery()
        query.exec("Use BookShare")
        query.exec("go")
        query.exec("exec update1 '%s',%f"%(current[0],rate))
        return 0


    def Btn_thunder(self):
        global url
        query = QSqlQuery()
        query.exec("Use BookShare")
        query.exec("go")
        print(current[0])
        query.exec("select * from dbo.updatedownloadtime ('%s')"%(current[0]))
        print(current)
        url = current[8]
        filename = current[1]+'.pdf'
        thunder = Dispatch('ThunderAgent.Agent64.1')
        thunder.AddTask(url, filename)
        thunder.CommitTasks()

    def Btn_rbook(self):
        self.stackedWidget.setCurrentIndex(1)
    def Btn_tutor(self):
        global id
        if(id==0):
            self.stackedWidget.setCurrentIndex(2)
            self.tutorstack.setCurrentIndex(1)
        else:
            self.stackedWidget.setCurrentIndex(2)
            self.tutorstack.setCurrentIndex(2)

    def Btn_refresh(self):
        self.vertification.setScaledContents(True)
        generate_captcha_image()
        global verify
        global path
        path = path + verify + '.png'
        print(path)
        jpg = QtGui.QPixmap(r'%s' % (path)).scaled(self.label.width(), self.label.height())
        self.vertification.setPixmap(jpg)


    def Btn_url(self):
        global url
        global code
        tiqucode =  "网盘地址为%s\n提取码为%s" % (url,code)
        mesBox = QMessageBox()
        mesBox.setWindowTitle('下载地址')
        mesBox.setText('%s'%tiqucode)
        mesBox.setIcon(QMessageBox.Information)
        mesBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        mesBox.setStyleSheet("QPushButton:hover{background-color: rgb(216, 227, 255);}")
        mesBox.exec_()
        self.setWindowTitle('百度网盘网页')
        self.setGeometry(5, 30, 1355, 730)
        self.browser = QWebEngineView()
        # 加载外部的web界面
        print(url)
        self.browser.load(QUrl('%s'%(url)))
        self.setCentralWidget(self.browser)


    def Btn_signup(self):
        self.tutorstack.setCurrentIndex(0)

    def Btn_fsignup(self):
        logid = self.logid.text()
        logpwd = self.logpwd.text()
        logrpwd = self.logrpwd.text()
        if (logpwd == logrpwd):
            query = QSqlQuery()
            query.exec("Use BookShare")
            query.exec("go")
            judge = query.exec("exec dbo.Input_info2_proc1 '%s','%s'"%(logid,logpwd))
            print(judge)
            if (judge == True):
                mesBox = QMessageBox()
                mesBox.setWindowTitle('注册')
                mesBox.setText(
                    '注册完成')
                mesBox.setIcon(QMessageBox.Information)
                mesBox.setStandardButtons(QMessageBox.Yes)
                mesBox.setStyleSheet("QPushButton:hover{background-color: rgb(216, 227, 255);}")
                mesBox.exec_()
                self.tutorstack.setCurrentIndex(1)
                self.rlogid.setText(logid)
                self.rlogpwd.setText(logpwd)
            elif(judge == False):
                mesBox = QMessageBox()
                mesBox.setWindowTitle('警告')
                mesBox.setText(
                    '该用户已被注册')
                mesBox.setIcon(QMessageBox.Information)
                mesBox.setStandardButtons(QMessageBox.Yes )
                mesBox.setStyleSheet("QPushButton:hover{background-color: rgb(216, 227, 255);}")
                mesBox.exec_()
                self.logid.setText("")
                self.logpwd.setText("")
                self.logrpwd.setText("")
        else:
            self.lab_warn.show()
            self.logrpwd.setText("")

    # 登录
    def Btn_signin(self):
        global id
        global verify
        self.btn_out.show()
        if (self.rlogid.text() == ""):
            self.logwarn.show()
            self.logwarn.setText("请输入账号")
        else:
            id = int(self.rlogid.text())
            pwd = self.rlogpwd.text()
            query = QSqlQuery()
            query.exec("Use BookShare")
            query.exec("go")
            print(id)
            query.exec("select dbo.Input_info_check('%d','%s')" % (id, pwd))
            while query.next():
                status = query.value(0)
            verified = self.verify.text()
            print(verified)
            print(verify)
            if (verified == verify and status == 1):
                status = 1
            elif(verified != verify and status == 1):
                status = 0



            if (status == 1):
                self.tutorstack.setCurrentIndex(2)
                self.welcome.setText("欢迎%d" % (id))
                query = QSqlQuery()
                query.exec("Use BookShare")
                query.exec("go")
                query.exec("select * from dbo.vx ('%d')" % (id))
                while query.next():
                    # 获取名称字段的值
                    vx = query.value(0)
                    print(vx)
                self.lab_vx.setText(vx)
                query.exec("select name from dbo.info where id = %d" % (id))
                while query.next():
                    # 获取名称字段的值
                    name = query.value(0)
                    print(name)
                self.lab_name.setText(name)
                query.exec("select dbo.Input_info_dnldtime1('%d')" % (id))
                while query.next():
                    dnld = query.value(0)
                    if (dnld != -1):
                        self.lab_dnld.setText(str(dnld) + '次')
                    else:
                        self.lab_dnld.setText("暂无")

                query.exec("select dbo.Input_info_rating('%d')" % (id))
                while query.next():
                    rating = query.value(0)
                    print(rating)
                    if (rating != -1):
                        self.lab_rate.setText(str(round(rating, 2)))
                    else:
                        self.lab_rate.setText("暂无")

                self.lab_profile.setText("%d" % (id))
                self.model = QSqlTableModel()
                self.mytable.setModel(self.model)
                self.mytable.verticalHeader().setVisible(False)
                self.mytable.horizontalHeader().setVisible(False)
                self.model.setTable('BookShare')
                query1 = "exec sellerpbook '%d' "%id
                query = QSqlQuery(query1)
                self.model.setQuery(query)
                self.model.query()
            elif (status == 0):
                self.logwarn.show()
                self.rlogpwd.setText("")
                self.verify.setText("")

    def Btn_namereverse(self):
        self.Le_name.show()
        self.btn_namefinish.show()
    def Btn_namefinish(self):
        global id
        print(id)
        self.btn_namefinish.hide()
        query = QSqlQuery()
        query.exec("Use BookShare")
        query.exec("go")
        name_reverse = self.Le_name.text()
        query.exec("exec updatename '%d','%s'" % (id, name_reverse))
        query.exec("select name from dbo.info where id = %d"%(id))
        while query.next():
            # 获取名称字段的值
            name = query.value(0)
            print(name)
        self.lab_name.setText(name)
        self.Le_name.hide()

    def Btn_vxreverse(self):#更新联系方式
        self.Le_vx.show()
        self.btn_vxfinish.show()
    def Btn_vxfinish(self):
        global id
        print(id)
        self.btn_vxfinish.hide()
        query = QSqlQuery()
        query.exec("Use BookShare")
        query.exec("go")
        vx_reverse = self.Le_vx.text()
        query.exec("exec vxupdate %d,%s"%(id,vx_reverse))
        query.exec("select * from dbo.vx ('%d')"%(id))
        while query.next():
            # 获取名称字段的值
            vx = query.value(0)
            print(vx)
        self.lab_vx.setText(vx)
        self.Le_vx.hide()

    def Btn_delete(self):
        row = self.mytable.currentIndex().row()
        delete = ['','','']
        if (row == -1):
            mesBox = QMessageBox()
            mesBox.setWindowTitle('警告')
            mesBox.setText(
                '上传纸质书籍/电子书籍请先登录')
            mesBox.setIcon(QMessageBox.Information)
            mesBox.setStandardButtons(QMessageBox.Yes )
            mesBox.setStyleSheet("QPushButton:hover{background-color: rgb(216, 227, 255);}")
            mesBox.exec_()
        else:
            for i in range(3):
                index = self.model.index(row, i)
                # self.model.removeRow(index.row())
                delete[i] = self.model.data(index)
            deleteid = delete[0]
            query = QSqlQuery()
            query.exec("Use BookShare")
            query.exec("go")
            query1 = "exec deletepb %s"%deleteid
            print(query1)
            query.exec("exec deletepb %s"%deleteid)



    def Btn_changeprofile(self):
        newicon = "./icons/%d.png"%(random.randint(1,20))
        self.photo.setPixmap(QtGui.QPixmap(newicon))
        self.uperprofile.setPixmap(QtGui.QPixmap(newicon))



    def List_subject(self):
        subject = self.Ebook_list.currentItem()
        major = subject.text()
        self.model = QSqlTableModel()
        self.showData.setModel(self.model)
        self.model.setTable('BookShare')
        query1 = "select * from Book where major = '%s'"%(major)
        print(query1)
        query = QSqlQuery(query1)
        self.model.setQuery(query)
        self.model.query()
    def Btn_search(self):
        global booktype
        booktype = self.combo_book.currentText()
        ebook_type = self.combo_type.currentText()
        condition = self.combo_condition.currentText()
        ebook_type = ebook_type[:-1]
        textsearch = self.Line_search.text()
        rateorder = self.rateorder.isChecked()
        dltimesorder = self.dltimesorder.isChecked()
        subject = self.Ebook_list.currentItem()
        major = subject.text()


        self.model = QSqlTableModel()
        self.showData.setModel(self.model)
        self.model.setTable('BookShare')  # 设置数据模型的数据表
        if (booktype == '实体书'):
            query1 = "select * from pbookview where b_name like '%" + "%s" % (textsearch) + "%'" +"and major = '%s'and pb_con = '%s' order by price desc"%(major,condition)
            print(query1)
            query = QSqlQuery(query1)
            self.model.setQuery(query)
            self.model.query()

        elif(booktype == '电子书'):
            if(rateorder == True and dltimesorder == False):
                query1 = "select * from ebookview where b_name like '%" + "%s" % (textsearch) + "%'" + " and eb_type='%s' and major = '%s' order by 'rating' desc" % (ebook_type,major)
            elif(rateorder == False and dltimesorder == True):
                query1 = "select * from ebookview where b_name like '%" + "%s" % (
                    textsearch) + "%'" + " and eb_type='%s' and major = '%s' order by 'dnldtime' desc" % (ebook_type,major)
            elif(rateorder == True and dltimesorder == True ):
                query1 = "select * from ebookview where b_name like '%" + "%s" % (
                    textsearch) + "%'" + " and eb_type='%s' and major = '%s' order by 'dnldtime','rating' desc" % (ebook_type,major)
            elif(rateorder == False and dltimesorder == False ):
                query1 = "select * from ebookview where b_name like '%" + "%s" % (
                    textsearch) + "%'" + " and eb_type='%s' and major = '%s' " % (ebook_type,major)

            print(query1)
            query = QSqlQuery(query1)
            self.model.setQuery(query)
            self.model.query()

    def Btn_upload(self):
        self.stackedWidget.setCurrentIndex(4)
        global id
        if(id == 0):
            mesBox = QMessageBox()
            mesBox.setWindowTitle('警告')
            mesBox.setText(
                '上传纸质书籍/电子书籍请先登录')
            mesBox.setIcon(QMessageBox.Information)
            mesBox.setStandardButtons(QMessageBox.Yes)
            mesBox.setStyleSheet("QPushButton:hover{background-color: rgb(216, 227, 255);}")
            mesBox.exec_()
            self.stackedWidget.setCurrentIndex(2)
    def Btn_uploadrate(self):
        return 0
    def Btn_donate(self):
        global id
        #获取最新的b_id
        query = QSqlQuery()
        query.exec("Use BookShare")
        query.exec("go")
        query.exec("Select b_id from Book")
        while query.next():
            b_id.append(query.value("b_id"))
        b_id.sort()
        b_id_max = b_id[-1:]
        b_max = b_id_max[0]
        b_new = 'b'+str(int(b_max[-5:])+1)
        #获取最新的eb_id
        query = QSqlQuery()
        query.exec("Use BookShare")
        query.exec("go")
        query.exec("Select eb_id from E_Book")
        while query.next():
            eb_id.append(query.value("eb_id"))
        eb_id.sort()
        eb_id_max = eb_id[-1:]
        eb_max = eb_id_max[0]
        eb_new = 'eb' + str(int(eb_max[-5:]) + 1)
        print(eb_new)
        #pb_id
        query = QSqlQuery()
        query.exec("Use BookShare")
        query.exec("go")
        query.exec("Select pb_id from P_Book")
        while query.next():
            pb_id.append(query.value("pb_id"))
        b_id.sort()
        pb_id_max = pb_id[-1:]
        pb_max = pb_id_max[0]
        pb_new = 'pb' + str(int(pb_max[-5:]) + 1)
        print(pb_new)
        type = self.comtype.currentText()
        print(type)
        if(type == '电子书'):
            bookname = self.lubookname.text()
            wri = self.luwri.text()
            pub = self.lupub.text()
            course = self.lucourse.text()
            major = self.commajor.currentText()
            edi = self.luedi.text()
            url = self.luurl.text()
            plat = self.luplatform.text()
            u_type=self.comu_type.currentText()
            code = self.lucode.text()
            eb_type=self.comeb_type.currentText()
            query = QSqlQuery()
            query.exec("Use BookShare")
            query.exec("go")
            query.exec("exec uploadebook %d,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s'"%(id,bookname,wri,pub,course
                                                        ,major,edi,eb_new,b_new,url,plat,u_type,code,eb_type))
            mesBox = QMessageBox()
            mesBox.setWindowTitle('上传')
            mesBox.setText(
                '上传成功')
            mesBox.setIcon(QMessageBox.Information)
            mesBox.setStandardButtons(QMessageBox.Yes)
            mesBox.setStyleSheet("QPushButton:hover{background-color: rgb(216, 227, 255);}")
            mesBox.exec_()
        elif type=="实体书":
            bookname = self.lubookname.text()
            wri = self.luwri.text()
            pub = self.lupub.text()
            course = self.lucourse.text()
            major = self.commajor.currentText()
            price = int(self.luprice.text())

            condi = self.comcondi.currentText()
            edi = self.luedi.text()
            query = QSqlQuery()
            query.exec("Use BookShare")
            query.exec("go")
            query.exec("exec uploadpaperbook '%d','%s','%s','%s','%s','%s',%d,'%s','%s','%s','%s'"%(id,bookname,wri,pub,course,major,price,condi,edi,pb_new,b_new))
            mesBox = QMessageBox()
            mesBox.setWindowTitle('上传')
            mesBox.setText(
                '上传成功')
            mesBox.setIcon(QMessageBox.Information)
            mesBox.setStandardButtons(QMessageBox.Yes)
            mesBox.setStyleSheet("QPushButton:hover{background-color: rgb(216, 227, 255);}")
            mesBox.exec_()


    #上传界面设置
    def Combo_type(self,text):
        if text=="实体书":
            self.uurl.hide()
            self.luurl.hide()
            self.uplatform.hide()
            self.luplatform.hide()
            self.uu_type.hide()
            self.comu_type.hide()
            self.ucode.hide()
            self.lucode.hide()
            self.ueb_type.hide()
            self.comeb_type.hide()
            self.uprice.show()
            self.luprice.show()
            self.ucondi.show()
            self.comcondi.show()
        elif text=="电子书":
            self.uurl.show()
            self.luurl.show()
            self.uplatform.show()
            self.luplatform.show()
            self.uu_type.show()
            self.comu_type.show()
            self.ucode.show()
            self.lucode.show()
            self.ueb_type.show()
            self.comeb_type.show()
            self.uprice.hide()
            self.luprice.hide()
            self.ucondi.hide()
            self.comcondi.hide()
    def Commu_type(self,text):
        if text == "直链":
            self.ucode.hide()
            self.lucode.hide()
        elif text == "网盘":
            self.ucode.show()
            self.lucode.show()

    def Combo_condition(self,text):
        if text == '电子书':
            self.combo_condition.hide()
            self.rateorder.show()
            self.dltimesorder.show()
            self.combo_type.show()
        elif text == '实体书':
            self.combo_type.hide()
            self.combo_condition.show()
            self.rateorder.hide()
            self.dltimesorder.hide()

    def Slider_rate(self,rate):
        self.lab_curate.setText("%.2f" % (rate / 100) + "分")
    def Btn_out(self,rate):
        global id
        id = 0
        self.stackedWidget.setCurrentIndex(2)
        self.tutorstack.setCurrentIndex(1)
        self.welcome.setText("请登录")
        self.rlogid.setText("")
        self.rlogpwd.setText("")
        self.verify.setText("")
        self.btn_out.hide()
    def Btn_stat(self):
        major= []
        mean = []
        dnld = []
        query = QSqlQuery()
        query.exec("Use BookShare")
        query.exec("go")
        query.exec("exec varmajor")
        while query.next():
            # 获取名称字段的值
            major.append(query.value(0))
            mean.append(query.value(1))
            dnld.append(query.value(2))
        print(major)
        print(mean)
        print(dnld)






        self.test = MyFigure(width=10, height=10, dpi=100)
        self.scene = QGraphicsScene()  # 创建一个场景
        self.scene.addWidget(self.test)  # 将图形元素添加到场景中
        self.graphicsView.setScene(self.scene)  # 将创建添加到图形视图显示窗口
        self.graphicsView.show()
        # X = np.linspace(-np.pi, np.pi, 256, endpoint=True)
        # C, S = np.cos(X), np.sin(X)
        # plt.plot(X, C)
        # plt.plot(X, S)
        plt.subplot(1, 2, 1)
        plt.bar(range(len(major)), mean,tick_label=major,color='#CD853F')
        plt.title('电子书籍平均评分')
        for a, b in zip(range(len(major)), mean):
            plt.text(a, b,'%.2f' %b,ha='center',va='bottom',)
        # plot 2:
        plt.subplot(1, 2, 2)
        plt.bar(range(len(major)), dnld, tick_label=major, color='#CD853F')
        plt.title('电子书籍下载次数')
        for a, b in zip(range(len(major)), dnld):
            plt.text(a, b, '%d' % b, ha='center', va='bottom', )
        plt.suptitle("平台数据")
        plt.show()

    def Btn_help(self):
        mesBox = QMessageBox()
        mesBox.setWindowTitle('帮助')
        mesBox.setText(
            'Q&A\nQ:迅雷下载为何使用用不了？\nA:用户需要首先在迅雷官网中下载迅雷下载器才能进行直链的下载\nQ:为什么我的纸质书无法上传\nA:纸质书的价格必须为数字\nQ:为什么没有图片\nA:开发者学业繁重，下次一定！')
        mesBox.setIcon(QMessageBox.Information)
        mesBox.setStandardButtons(QMessageBox.Yes)
        mesBox.setStyleSheet("QPushButton:hover{background-color: rgb(216, 227, 255);}")
        mesBox.exec_()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    style_file = './qss/style.qss'
    style_sheet = QSSLoader.read_qss_file(style_file)
    mainWindow.setStyleSheet(style_sheet)
    mainWindow.show()
    sys.exit(app.exec())
