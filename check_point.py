import json
import requests
import urllib3

class Check_Point(object):
   def __init__(self,host,port,username,password):
      urllib3.disable_warnings()
      self.host = host
      self.port = port
      self.username = username
      self.password = password
      self.url_base = "https://{h}:{p}/web_api".format(h=self.host,p=self.port)
      self.login()

   def login(self):
      payload = { 'user':self.username,'password':self.password }
      url = "{u}/login".format(u=self.url_base)
      headers = { 'Content-Type':'application/json' }
      req = requests.post(url,json.dumps(payload),headers=headers,verify=False)
      req = req.json()
      self.sid = req["sid"]

   def api_call(self,command,payload):
      url = "{u}/{c}".format(u=self.url_base,c=command)
      headers = { 'Content-Type':'application/json','X-chkp-sid':self.sid }
      req = requests.post(url,json.dumps(payload),headers=headers,verify=False)
      req = req.json()
      return req
