# coding=utf8
import sys
import os
from PyQt5 import uic, QtCore, QtGui, QtWidgets
import smartqq.login

Ui_MainWindow, QtBaseClass = uic.loadUiType(os.getcwd() + '\\main.ui')

# 定义函数类
class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
  def __init__(self):
    # Qt初始化
    QtWidgets.QMainWindow.__init__(self)
    Ui_MainWindow.__init__(self)
    self.setupUi(self)

# 初始化程序
if __name__ == "__main__":
  app = QtWidgets.QApplication(sys.argv)
  window = MyApp()
  login = smartqq.login.Login(window)
  login.init()
  window.show()
  sys.exit(app.exec_())