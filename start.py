# coding=utf8
import sys
import os
from PyQt5 import uic, QtCore, QtGui, QtWidgets
import smartqq.login

if __name__ == '__main__':
  # 登录
  login = smartqq.login.Login()
  login.init()
  
  