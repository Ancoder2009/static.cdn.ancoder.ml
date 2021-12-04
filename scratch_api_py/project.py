import requests

class project:
    def __init__(self, info, project_id):
        self.pid = project_id
        self.info = info
        self.headers = {
                "x-csrftoken": "a",
                "x-requested-with": "XMLHttpRequest",
                "Cookie": "scratchcsrftoken=a;scratchlanguage=en;",
                "referer": "https://scratch.mit.edu",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36"
            }

    def getLoves(self):
        return requests.get(f"https://api.scratch.mit.edu/projects/{str(self.pid)}").json()["stats"]["loves"]
    
    def getFavorites(self):
        return requests.get(f"https://api.scratch.mit.edu/projects/{str(self.pid)}").json()["stats"]["favorites"]

    def getViews(self):
        return requests.get(f"https://api.scratch.mit.edu/projects/{str(self.pid)}").json()["stats"]["views"]
        
    def getRemixes(self):
        return requests.get(f"https://api.scratch.mit.edu/projects/{str(self.pid)}").json()["stats"]["remixes"]
        
    def shareProject(self):
        headers = {
                "x-csrftoken": self.info["csrf"],
                "Cookie": f"scratchcsrftoken={self.info['csrf']};scratchsessionsid={str(self.info['sessid'])};scratchlanguage=en;",
                "referer": f"https://scratch.mit.edu",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36 Edg/96.0.1054.34",
                "x-token": self.info["token"],
                "orgin": "https://scratch.mit.edu"
            }
        res = requests.put("https://api.scratch.mit.edu/proxy/projects/"+str(self.pid)+"/share", headers=headers)
