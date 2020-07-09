import requests


class HttpRequest(object):
    """直接发送请求不记录cookies"""
    def request(self, url, method, data=None, headers=None):
        method = method.lower()
        if method == 'get':
            return requests.get(url=url, params=data, headers=headers)
        elif method == 'post':
            return requests.post(url=url, data=data, headers=headers)

class HttpSession(object):
    """发送请求并记录cookies"""
    def __init__(self):
        self.session = requests.session()

    def request(self, url, method, data=None, headers=None, json=None):
        method = method.lower()
        if method == 'get':
            return self.session.get(url=url, params=data, headers=headers, json=json)
        elif method == 'post':
            return self.session.post(url=url, data=data, headers=headers, json=json)

    def close(self):
        self.session.close()


http_request = HttpRequest()
# if __name__ == '__main__':
#     r1 = http_request.request('http://api.keyou.site:8000/user/register/', 'post', {'username': '999999','email': 'email@qq.com','password':'123456','password_confirm': '123456'})
#     print(type(r1.status_code))
