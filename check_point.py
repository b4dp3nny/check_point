import json
import requests

class Check_Point(object):
    __init__(self,host,port,username,password,command={}):
       self.host = host
       self.port = port
       self.username = username
       self.password = password
       self.command = json.dumps(command)
       
