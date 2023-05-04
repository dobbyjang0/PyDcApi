from src.session.login import login

class AnonymousUser:
    def __init__(self, id='ㅇㅇ', password='1234'):
        self.type = "anonymous"
        self.id = id
        self.password = password

class LoginUser:
    def __init__(self, id, password):
        self.type = "login"
        self.id = id
        self.password = password
        self.is_login = False
        self.cookie = None

    async def login(self):
        if self.is_login:
            print('이미 로그인 되어있습니다.')

        self.cookie = await login(self.id, self.password)
        self.is_login = True
