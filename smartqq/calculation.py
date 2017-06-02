# coding=utf8
# 算法
import time

# 解密
def hash33(t):
  e = 0
  i = 0
  n = len(t)
  while n > i:
    e += (e << 5) + ord(t[i])
    i += 1
  return 2147483647 & e


# hash加密算法，传递参数为uin和pywebqq
def hash(uin, ptwebqq):
  N = [0, 0, 0, 0]
  t = 0
  k = len(ptwebqq)
  while t < k:
    N[t % 4] ^= ord(ptwebqq[t])
    t += 1
  
  U = ['EC', 'OK']
  V = [0, 0, 0, 0]
  V[0] = uin >> 24 & 255 ^ ord(U[0][0])
  V[1] = uin >> 16 & 255 ^ ord(U[0][1])
  V[2] = uin >> 8 & 255 ^ ord(U[1][0])
  V[3] = uin & 255 ^ ord(U[1][1])
  
  U1 = [0, 0, 0, 0, 0, 0, 0, 0]
  t1 = 0
  k1 = len(U1)
  while t1 < k1:
    if t1 % 2 == 0:
      U1[t1] = N[t1 >> 1]
    else:
      U1[t1] = V[t1 >> 1]
    t1 += 1
  
  N1 = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
  V1 = ''
  for aU1 in U1:
    V1 += N1[(aU1 >> 4) & 15]
    V1 += N1[aU1 & 15]
  
  return V1


# 获取cookie
def getCookie(cookiejar, key):
  x = None
  for item in cookiejar:
    if key == item.name:
      x = item.value
      break
  return x


# 查询gnamelist内的群信息
def getGName(gnamelist, name):
  x = None
  for item in gnamelist:
    if item['name'] == name:
      x = item
      break
  return x


# 计算msg_id
sequence = 0
t = time.time() * 100
t = (t - t % 1000) / 1000
t = t % 10000 * 10000

def msgId():
  global t, sequence
  sequence += 1
  return int(t + sequence)