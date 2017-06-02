# coding=utf8
import random

api = {
  # 二维码图片地址
  # 请求方式：get
  # 参数：t -> 随机数
  # cookie里面返回令牌token
  'ptqr': 'https://ssl.ptlogin2.qq.com/ptqrshow?appid=501004106&e=0&l=M&s=5&d=72&v=4&t=',
  
  # login判断
  # 请求方式：get
  # 参数：ptqrtoken -> 解密后的令牌
  # cookie里面返回ptwebqq
  'isLogin': 'https://ssl.ptlogin2.qq.com/ptqrlogin?webqq_type=10&remember_uin=1' +
             '&login2qq=1&aid=501004106&u1=http%3A%2F%2Fw.qq.com%2Fproxy.html%3Flogin2qq%3D1%26webqq_type%3D10' +
             '&ptredirect=0&ptlang=2052&daid=164&from_ui=1&pttype=1&dumy=&fp=loginerroralert&action=0-0-2105' +
             '&mibao_css=m_webqq&t=undefined&g=1&js_type=0&js_ver=10220&login_sig=&pt_randsalt=0&ptqrtoken=',
  
  # 获取vfwebqq
  # 请求方式：get
  'vfwebqq': 'http://s.web2.qq.com/api/getvfwebqq?clientid=53999199&psessionid=&t=' +
             str(random.randint(100000000000, 999999999999)) +
             '&ptwebqq=',
  
  # 获取psessionid和uin
  # 请求方式：post
  'uin': 'http://d1.web2.qq.com/channel/login2',
  
  # 获取group
  # 请求方式post
  'group': 'http://s.web2.qq.com/api/get_group_name_list_mask2',
  
  # 获取在线好友列表
  # 请求方式post
  'friends': 'http://d1.web2.qq.com/channel/get_online_buddies2',
  
  # 发送数据接口
  # 请求方式：post
  'send': 'https://d1.web2.qq.com/channel/send_qun_msg2',
  
  # 获取数据接口
  # 请求方式：post
  'poll2': 'https://d1.web2.qq.com/channel/poll2',
}