# @Time    :2018/10/29 16:57
# @Author  :lvjunjie
import hashlib
import re

import requests


class LoginApi(object):
    @staticmethod
    def logindmp(username, password):
        """
        dmp平台账号密码登录
        """
        session_sso = requests.Session()
        cookie = {
            "OUTFOX_SEARCH_USER_ID_NCOO": "2139139465.580414"
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, "
                          "like Gecko) Chrome/70.0.3538.77 Safari/537.36",
        }
        res_sso = session_sso.get(url='http://bops.test.tthunbohui.com', headers=headers, cookies=cookie)
        test_sso = res_sso.text
        lt = re.search("name=\"lt\" value=\"(.+?)\"", test_sso).group(1)
        Set_Cookie = res_sso.headers["Set-Cookie"]
        JSESSIONID = Set_Cookie[11:43]
        params = {
            'service': 'http://bops.test.tthunbohui.com/'
        }
        data = {
            "username": username,
            "password": LoginApi.computeMD5hash(password),
            "vcode": 1,
            "lt": lt,
            "execution": 'e1s1',
            "_eventId": 'submit',
            "submit": '%E7%99%BB%E5%BD%95'
        }
        headers = {
            "Cache-Control": 'max-age=0',
            "Content-Type": 'application/x-www-form-urlencoded',
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                          'like Gecko) Chrome/70.0.3538.77 Safari/537.36',
        }
        res2 = session_sso.post(url='http://sso.test.tthunbohui.com' + '/login;jsessionid=' + JSESSIONID, params=params,
                                data=data, headers=headers, cookies=cookie, allow_redirects=False)
        cookies = res2.cookies
        for cookie in cookies:
            if cookie is not None and str(cookie.name) == "CASTGC":
                # 登录认证成功获取TGC票据
                print("CASTGC:" + str(cookie.value) + "用户登录认证成功,并获取TGC票据")
        # print("res2" + str(res2.content.decode('utf-8')))
        res__headers = res2.headers
        for header in res__headers:
            print(res__headers[str(header)])
        Location = res__headers['Location']
        res1 = session_sso.get(url=Location, allow_redirects=False)
        # 获取ST
        st_cookie_list = res1.cookies
        for cookie in st_cookie_list:
            if cookie is not None and str(cookie.name) == "SESSION":
                # 登录认证成功获取ST票据
                print("session:" + str(cookie.value) + "用户登录认证成功,生成session")
        # print("res1" + str(res1.content.decode('utf-8')))
        Location = res1.headers['Location']
        res = session_sso.get(url=Location, allow_redirects=False)
        # 打印解码数据
        # print("res" + str(res.content.decode('utf-8')))
        return res, res1, res2

    @staticmethod
    def computeMD5hash(my_string):
        # md5加密
        m = hashlib.md5()
        m.update(my_string.encode('utf-8'))
        return m.hexdigest()


LoginApi.logindmp("18000000000", "123456")
