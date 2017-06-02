# coding=utf8
import http.cookiejar
import json
import random
import re
import threading
import time
import urllib.parse
import urllib.request
from PyQt5 import QtGui
from smartqq.api import api
from smartqq.calculation import hash33, hash, getCookie, getGName, msgId

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36'
  
# 登录
class Login:
  def __init__(self, window):
    self.cookiejar = http.cookiejar.CookieJar()      # cookiejar
    self.opener = urllib.request.build_opener(       # opener
                  urllib.request.HTTPCookieProcessor(self.cookiejar))
    
    self.token = None                                # 二维码登录令牌
    self.image = None                                # 二维码
    
    self.name = None                                 # 登录的用户名
    self.ptwebqq = None                              # ptwebqq
    self.vfwebqq = None                              # vfwebqq
    self.psessionid = None                           # psessionid
    self.uin = None                                  # uin
    self.cip = None                                  # cip
    
    self.gnamelist = None                            # 获取群列表
    self.friends = None                              # 获取在线好友列表
    
    self.state = 0                                   # 当前登录状态
    self.timer = threading.Timer(1, self.timerLogin) # 当前定时器
    
    self.window = window                             # window窗口实例

  ### 这部分用于二维码相关

  # 下载二维码图片
  def downloadPtqr(self):
    request = urllib.request.Request(api['ptqr'] + str(random.random()), headers={
      'Connection': 'keep-alive',
      'User-Agent': USER_AGENT,
    })
    response = self.opener.open(request)
    self.image = response.read()
  
  # 将二维码图片写入缓存文件夹
  def writePtqr(self):
    file = open('./.cache/_ptqr_165x165.png', 'wb')
    file.write(self.image)
    file.close()
    # PyQt@显示图片
    path = QtGui.QPixmap('./.cache/_ptqr_165x165.png')
    self.window.SmartQQ.setPixmap(path)

  # 计算令牌
  def getToken(self):
    qrsig = getCookie(self.cookiejar, 'qrsig')
    self.token = hash33(qrsig)

  def initPtQr(self):
    self.downloadPtqr()
    self.writePtqr()
    self.getToken()
    
  ### 轮询二维码状态
  
  # 定时器
  def timerLogin(self):
    if self.state == 0:
      self.isLogin()
      self.timer = threading.Timer(.5, self.timerLogin)
      self.timer.start()

  # 取出ptwebqq
  def getPyWebQQ(self):
    ptwebqq = getCookie(self.cookiejar, 'ptwebqq')
    self.ptwebqq = ptwebqq
  
  # 判断登录状态
  def isLogin(self):
    request = urllib.request.Request(api['isLogin'] + str(self.token), headers={
      'Connection': 'keep-alive',
      'User-Agent': USER_AGENT,
    })
    response = self.opener.open(request)
    
    """
    数组索引的代表：
    【1】：二维码状态，未失效->66，失效->65
    【4】：文字提示：未失效->'二维码未失效。'
    """
    RE = re.compile(r'[^\'",()]+', re.I)
    res = response.read().decode()
    res2 = RE.findall(res)

    # 失效时重新获取二维码
    if res2[1] == '65':
      self.initPtQr()
    # 获取到二维码状态
    elif res2[1] == '0':
      self.name = res2[7]
      self.getPyWebQQ()
      # 登录
      self.initLogin(res2[3])
      self.state = 1
  
  ### 登陆
  
  # 登陆
  def login(self, url):
    request = urllib.request.Request(url, headers={
      'Connection': 'keep-alive',
      'User-Agent': USER_AGENT,
    })
    response = self.opener.open(request)

  # 获取vfwebqq
  def getVfWebQQ(self):
    url = api['vfwebqq'] + self.ptwebqq
    request = urllib.request.Request(url, headers={
      'Referer': 'http://s.web2.qq.com/proxy.html?v=20130916001&callback=1&id=1',
      'Connection': 'keep-alive',
      'User-Agent': USER_AGENT,
    })
    response = self.opener.open(request)
    obj = json.loads(response.read().decode())
    self.vfwebqq = obj['result']['vfwebqq']
    
  # 获取psessionid和uin
  def getPsessionAndUin(self):
    data = urllib.parse.urlencode({
      'r': '{"ptwebqq": "' + self.ptwebqq + '", "clientid": 53999199, "psessionid": "", "status": "online"}'
    })
    request = urllib.request.Request(api['uin'], data=data.encode('utf-8'), headers={
      'Referer': 'http://d1.web2.qq.com/proxy.html?v=20151105001&callback=1&id=2',
      'Connection': 'keep-alive',
      'User-Agent': USER_AGENT,
    })
    response = self.opener.open(request)
    obj = json.loads(response.read().decode())
    self.psessionid = obj['result']['psessionid']
    self.uin = obj['result']['uin']
    self.cip = obj['result']['cip']
  
  def initLogin(self, url):
    self.login(url)
    self.getPyWebQQ()
    self.getPsessionAndUin()
    self.initSuccess()
      
  ### 登录成功事件
  
  # 获取群组
  def getGroup(self):
    data = urllib.parse.urlencode({
      'r': '{"vfwebqq":"' + str(self.vfwebqq) + '","hash":"' + hash(self.uin, self.ptwebqq) + '"}',
    })
    request = urllib.request.Request(api['group'], data=data.encode('utf-8'), headers={
      'Referer': 'http://s.web2.qq.com/proxy.html?v=20130916001&callback=1&id=1',
      'Content-Type': 'application/x-www-form-urlencoded',
      'Connection': 'keep-alive',
      'User-Agent': USER_AGENT,
    })
    response = self.opener.open(request)
    obj = json.loads(response.read().decode())
    self.gnamelist = obj['result']['gnamelist']
    
  # 获取在线好友列表
  def getFriends(self):
    url = api['friends'] + '?vfwebqq=' + str(self.vfwebqq) + '&clientid=53999199&psessionid=' + self.psessionid + '&t=' + str(time.time())
    request = urllib.request.Request(url, headers={
        'Referer': 'http://d1.web2.qq.com/proxy.html?v=20151105001&callback=1&id=2',
        'User-Agent': USER_AGENT,
    })
    response = self.opener.open(request)
    obj = json.loads(response.read().decode())
    self.friends = obj['result']
  
  # 登录成功后执行的函数
  def loginSuccess(self):
    # PyQt@图片改成登录信息
    self.window.SmartQQ.setText('QQ：' + str(self.uin) + '\n用户名：' + self.name)
    self.window.SmartQQ2.setText('')
    # 其他事件

  def initSuccess(self):
    self.getFriends()
    self.getGroup()
    self.loginSuccess()
  
  # 获取数据
  def getMessage(self):
    data = urllib.parse.urlencode({
      'r': '{"ptwebqq": "' + self.ptwebqq + '", "clientid": 53999199, "psessionid": "' + self.psessionid + '", "key": ""}',
    })
    request = urllib.request.Request(api['poll2'], data=data.encode('utf-8'), headers={
      'Content-Type': 'application/x-www-form-urlencoded',
      'Host': 'd1.web2.qq.com',
      'Origin': 'https://d1.web2.qq.com',
      'Referer': 'https://d1.web2.qq.com/cfproxy.html?v=20151105001&callback=1',
    })
    response = self.opener.open(request)
    """
    result[0]:
      poll_type: "group_message"
      value:
        content[1]:               接收到的信息
        from_uin: 1398039796      信息来自的群
        group_code: 1398039796
        msg_id: 27127
        msg_type: 4
        send_uin: 4129086259      发信息的群员的编号
        time: 1496305408
        to_uin:
    """
    obj = json.loads(response.read().decode())
    return obj
    
  # 发送数据
  def sendGroupMessage(self, groupName, message):
    # 发送数据
    item = getGName(self.gnamelist, groupName)
    data = urllib.parse.urlencode({
      'r': '{"group_uin":' + str(item['gid']) + ',"content":"' +
           '[\\"' + message + '\\",[\\"font\\",{\\"name\\":\\"宋体\\",\\"size\\":10,\\"style\\":[0,0,0],\\"color\\":\\"000000\\"}]]",' +
           '"face":333,"clientid":53999199,"msg_id":' + str(msgId()) + ',"psessionid":"' + self.psessionid + '"}',
    })
    request = urllib.request.Request(api['send'], data=data.encode('utf-8'), headers={
      'Referer': 'https://d1.web2.qq.com/cfproxy.html?v=20151105001&callback=1',
      'Content-Type': 'application/x-www-form-urlencoded',
      'Connection': 'keep-alive',
      'User-Agent': USER_AGENT,
    })
    response = self.opener.open(request)  # {"errCode":0,"msg":"send ok"}
    
  # 初始化
  def init(self):
    self.initPtQr()     # 二维码
    self.timer.start()  # 登录轮询