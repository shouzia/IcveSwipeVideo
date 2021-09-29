from io import BytesIO
from PIL import Image
import time
import base64
import random
import json
import sys
import math
import requests


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,like Gecko) '
                         'Chrome/86.0.4240.75 Safari/537.36'}


class Mooc:
    def __init__(self):
        self.username = input("请输入您的账号:")
        self.password = input("请输入您的密码:")
        self.verifyCode = None
        self.session = requests.session()
        self.verify()
        self.login()

    def verify(self):
        codeContent = self.session.get(f'https://www.icve.com.cn/portal/VerifyCode/index?t={random.random()}',
                                       headers=headers).content
        byteIoObj = BytesIO()
        byteIoObj.write(codeContent)
        Image.open(byteIoObj).show()
        self.verifyCode = input('请输入验证码：')

    def login(self):
        data = {'userName': base64.b64encode(self.username.encode()),
                'pwd': base64.b64encode(self.password.encode()),
                'verifycode': self.verifyCode}
        res = self.session.post(
            'https://www.icve.com.cn/portal/Register/Login_New', headers=headers, data=data).text
        _json = json.loads(res)
        if _json['code'] == 1:
            cookie = str(requests.utils.dict_from_cookiejar(
                self.session.cookies))
            cookie1 = cookie.split('\'')[3]
            print('登录成功')
            return cookie1
        else:
            print(_json['msg'])
            sys.exit(-1)
