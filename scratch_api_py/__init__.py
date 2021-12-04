import requests
import os
import json
import re
from . import API_ERRORS

class Session:
    def __init__(self, username: str, password: str):
        self.user = username
        self.passw = password
        self.credentials = {"usr": self.user, "pass": self.passw, "sessid": None, "csrf": None, "token": None}
        self.ready = False

    def login(self):
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36 Edg/96.0.1054.34"
        self.headers = {
            "x-csrftoken": "a",
            "x-requested-with": "XMLHttpRequest",
            "Cookie": "scratchcsrftoken=a;scratchlanguage=en;",
            "referer": "https://scratch.mit.edu",
            "user-agent": self.user_agent
        }

        data = json.dumps({
                "username": self.user,
                "password": self.passw
            })

        res = requests.post(
                'https://scratch.mit.edu/login/', data=data, headers=self.headers)
        if not 'token' in res.json()[0]:
            raise API_ERRORS.AuthentificatonFailed("Username or password is not correct, login failed!")
        else:
            self.credentials["token"] = res.json()[0]["token"]
            self.credentials["sessid"] = re.search('\"(.*)\"', res.headers["Set-Cookie"]).group()
            self.credentials["csrf"] = re.search("scratchcsrftoken=(.*?);", res.headers["Set-Cookie"]).group(1)
            self.ready = True

    def Cloud(self, project_id):
        try:
            if self.ready:
                from . import cloud
                return cloud.cloud(self.credentials, project_id)
            else:
                raise API_ERRORS.NotReady("Try logging in using obj.login()")
        except ImportError:
            raise API_ERRORS.PackageError("Package cloud is not installed.")
    def Project(self, project_id):
        try:
            if self.ready:
                from . import project
                return project.project(self.credentials, project_id)
            else:
                raise API_ERRORS.NotReady("Try logging in using obj.login()")
        except ImportError:
            raise API_ERRORS.PackageError("Package project is not installed.")
