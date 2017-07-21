# coding=utf8
import threading
from smartQQ import Login
from calculation import getGName

GROUP_NAME = '' # 群组名称
smartqq = Login(GROUP_NAME)

# 二维码相关
smartqq.downloadPtqr()
smartqq.writePtqr()
smartqq.getToken()

# 登录成功后的事件
def loginSuccessCb():
  smartqq.state = 1
  smartqq.login()
  smartqq.getVfWebQQ()
  smartqq.getPsessionAndUin()
  smartqq.getFriends()
  smartqq.getGroup()
  smartqq.item = getGName(smartqq.gnamelist, smartqq.groupname)
  timerForLoginReset.start()
  print('Message: 登录成功')
  print('Message: name -> ' + smartqq.name)
  print('Message: uin  -> ' + str(smartqq.uin))
  smartqq.sendGroupMessage(smartqq.token)
  timerGetMessage.start()

# 重新登录
def loginReset():
  global timerForLoginReset
  timerForLoginReset = threading.Timer(600, loginReset)
  timerForLoginReset.start()
  smartqq.loginBrokenLineReconnection()
  smartqq.item = getGName(smartqq.gnamelist, GROUP_NAME)
  
timerForLoginReset = threading.Timer(600, loginReset)

# 轮询登录状态
def timerLogin():
  global timerForLogin
  if smartqq.state == 0:
    smartqq.isLogin(loginSuccessCb)
    timerForLogin = threading.Timer(1, timerLogin)
    timerForLogin.start()
    
timerForLogin = threading.Timer(1, timerLogin)
timerForLogin.start()

# 轮询获取数据
def getMessage():
  global timerGetMessage
  timerGetMessage = threading.Timer(1, getMessage)
  timerGetMessage.start()
  msg = smartqq.getMessage()
  
timerGetMessage = threading.Timer(1, getMessage)