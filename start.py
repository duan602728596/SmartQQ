# coding=utf8
import sys
import os
from PyQt5 import uic, QtCore, QtGui, QtWidgets
import smartqq.login

# ui地址
Ui_MainWindow, QtBaseClass = uic.loadUiType(os.getcwd() + '\\main.ui')


# 定义函数类
class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
  def __init__(self):
    # Qt初始化
    QtWidgets.QMainWindow.__init__(self)
    Ui_MainWindow.__init__(self)
    self.setupUi(self)

if __name__ == '__main__':
  app = QtWidgets.QApplication(sys.argv)
  window = MyApp()
  window.show()
  sys.exit(app.exec_())
  # 登录
  # login = smartqq.login.Login()
  # login.init()
  
  