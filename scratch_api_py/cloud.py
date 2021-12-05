try:
    import websocket #upm package(websocket-client)
except ImportError:
    import os
    os.system("pip install websocket-client")
import json
import requests
from . import API_ERRORS

class cloud:
    def __init__(self, info, project_id):
        self.info = info
        self.project_id = str(project_id)
        self.ready = False
    
    def Open(self):
        self.ws = websocket.WebSocket()
        self.connect()

        self.ready = True
    def connect(self):
        self.ws.connect("wss://clouddata.scratch.mit.edu", cookie=f"scratchsessionsid={self.info['sessid']};", orgin="https://scratch.mit.edu", enable_multithread=True)

        self.ws.send(f"{json.dumps({'method': 'handshake', 'user': self.info['usr'], 'project_id': self.project_id})}\n")

    def setVar(self, var, val):
        var = f"☁ {str(var)}"
        if self.ready:
            try:
                self.ws.send(f"{json.dumps({'method': 'set', 'name': var, 'value': str(val), 'user': self.info['usr'], 'project_id': self.project_id})}\n")
            except BrokenPipeError:
                self.connect()
                self.ws.send(f"{json.dumps({'method': 'set', 'name': var, 'value': str(val), 'user': self.info['usr'], 'project_id': self.project_id})}\n")
        else:
            raise API_ERRORS.NotReady("Connection not open try obj.Open()!")
    
    def varExists(self, var):
        if self.getVar(var) != None:
            return True
        else:
            return False

    def getVar(self, var):
        
        res = requests.get(f"https://clouddata.scratch.mit.edu/logs?projectid={self.project_id}&limit=1567&offset=0")
        while res.status_code == 502:
            res = requests.get(f"https://clouddata.scratch.mit.edu/logs?projectid={self.project_id}&limit=1567&offset=0")

        res = res.json()
        var = f"☁ {str(var)}"
        for i in res:
            if var == i["name"]:
                return i["value"]
    
    def close(self):
        self.ws.close()

    def encodeData(self, data : str):
        string = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()_-+=[]{}\\\"'/?.,<>:"
        encoded = ""

        for i in data:
            if i in string:
                index = string.find(i)
                if index < 10:
                    index = "0" + str(index)
                encoded += str(index)
        
        return encoded
    
    def decodeData(self, data : str):
        string = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()_-+=[]{}\"'/?.,<>:"
        decoded = ""

        for i in range(0, len(data), 2):
            current_num = data[i] + data[i + 1]
            current_num = int(current_num)

            decoded += string[current_num]
        
        return decoded
