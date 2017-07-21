# coding=utf8
# smartQQ接口

import http.cookiejar
import json
import random
import re
import time
import urllib.parse
import urllib.request
from api import api
from calculation import hash33, hash, getCookie, getGName, msgId

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36'

# smartqq登录
class Login:
  def __init__(self, groupname):
    self.cookiejar = http.cookiejar.CookieJar()        # cookiejar
    self.opener = urllib.request.build_opener(         # opener
      urllib.request.HTTPCookieProcessor(self.cookiejar))
    
    self.token = None                                  # 二维码登录令牌
    self.image = None                                  # 二维码
    self.url = None                                    # 登录url
    
    self.name = None                                   # 登录的用户名
    self.ptwebqq = None                                # ptwebqq
    self.vfwebqq = None                                # vfwebqq
    self.psessionid = None                             # psessionid
    self.uin = None                                    # uin
    self.cip = None                                    # cip
    
    self.gnamelist = None                              # 获取群列表
    self.friends = None                                # 获取在线好友列表
    
    self.state = 0                                     # 当前登录状态
    self.groupname = groupname                         # 群名称

  # 下载二维码图片
  def downloadPtqr(self):
    request = urllib.request.Request(api['ptqr'] + str(random.random()), headers={
      'Connection': 'keep-alive',
      'User-Agent': USER_AGENT,
    })
    response = self.opener.open(request)
    self.image = response.read()
    print('Message: 二维码下载成功')

  # 将二维码图片写入缓存文件夹
  def writePtqr(self):
    file = open('./a扫描二维码快点别过期了.png', 'wb')
    file.write(self.image)
    file.close()
    print('Message: 扫描二维码')
    
  # 计算令牌
  def getToken(self):
    qrsig = getCookie(self.cookiejar, 'qrsig')
    self.token = hash33(qrsig)
    print('Message: 计算令牌')

  # 取出ptwebqq
  def getPyWebQQ(self):
    ptwebqq = getCookie(self.cookiejar, 'ptwebqq')
    self.ptwebqq = ptwebqq
    
  # 判断登录状态
  def isLogin(self, callback):
    request = urllib.request.Request(api['isLogin'] + str(self.token), headers={
      'Connection': 'keep-alive',
      'User-Agent': USER_AGENT,
    })
    response = self.opener.open(request)
  
    RE = re.compile(r'[^\'",()]+', re.I)
    res = response.read().decode()
    res2 = RE.findall(res)
  
    # 失效时重新获取二维码
    if res2[1] == '65':
      self.downloadPtqr()
      self.writePtqr()
      self.getToken()
    # 获取到二维码状态
    elif res2[1] == '0':
      self.name = res2[7]
      self.getPyWebQQ()
      self.url = res2[3]
      callback()
      self.state = 1
  
  # 登陆
  def login(self):
    request = urllib.request.Request(self.url, headers={
      'Connection': 'keep-alive',
      'User-Agent': USER_AGENT,
    })
    response = self.opener.open(request)

  # 重新登录
  def loginBrokenLineReconnection(self):
    self.login()
    self.getVfWebQQ()
    self.getPsessionAndUin()
    self.getFriends()
    self.getGroup()
    self.item = getGName(self.gnamelist, self.groupname)  # 获取群信息

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

  # 获取群组
  def getGroup(self):
    try:
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
      print('Message: 获取群组')
    except:
      self.getGroup()

  # 获取在线好友列表
  def getFriends(self):
    try:
      url = api['friends'] + '?vfwebqq=' + str(
        self.vfwebqq) + '&clientid=53999199&psessionid=' + self.psessionid + '&t=' + str(time.time())
      request = urllib.request.Request(url, headers={
        'Referer': 'http://d1.web2.qq.com/proxy.html?v=20151105001&callback=1&id=2',
        'User-Agent': USER_AGENT,
      })
      response = self.opener.open(request)
      obj = json.loads(response.read().decode())
      self.friends = obj['result']
      print('Message: 获取在线好友列表')
    except:
      self.friends = []

  # 获取数据
  def getMessage(self):
    try:
      data = urllib.parse.urlencode({
        'r': '{"ptwebqq": "' + self.ptwebqq + '", "clientid": 53999199, "psessionid": "' + self.psessionid + '", "key": ""}',
      })
      request = urllib.request.Request(api['poll2'], data=data.encode('utf-8'), headers={
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'd1.web2.qq.com',
        'Origin': 'https://d1.web2.qq.com',
        'Referer': 'https://d1.web2.qq.com/cfproxy.html?v=20151105001&callback=1',
        'Connection': 'keep-alive',
      })
      response = self.opener.open(request, timeout=60)  # 60秒后收不到消息切断连接
      obj = json.loads(response.read().decode())
      return obj
    except:
      return {}

  # 发送数据
  def sendGroupMessage(self, message):
    # 发送数据
    try:
      data = urllib.parse.urlencode({
        'r': '{"group_uin":' + str(self.item['gid']) + ',"content":"' +
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
    except:
      pass