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
   #Main Check Point interaction function.
   def api_call(self,command,payload={}):
      url = "{u}/{c}".format(u=self.url_base,c=command)
      headers = { 'Content-Type':'application/json','X-chkp-sid':self.sid }
      req = requests.post(url,json.dumps(payload),headers=headers,verify=False)
      req = req.json()
      return req
   #Session management.
   def login(self):
      payload = { 'user':self.username,'password':self.password }
      url = "{u}/login".format(u=self.url_base)
      headers = { 'Content-Type':'application/json' }
      req = requests.post(url,json.dumps(payload),headers=headers,verify=False)
      req = req.json()
      #Create sid variable to be used in all authenticated interactions.s
      self.sid = req["sid"]

   def show_session(self):
      req = self.api_call('show-session')
      return req

   def discard_expired_sessions(self):
      payload = { 'details-level':'full' }
      all_sessions = self.api_call('show-sessions',payload)
      number_discarded = 0
      #Iterate through objects in all_sessions.
      for s in all_sessions["objects"]:
         #Check for expired-session == true and discard.
         if s["expired-session"]:
            payload = { "uid":s["uid"]}
            req = self.api_call('discard',payload)
            number_discarded += 1
      message = "{n} sessions have been discarded".format(n=number_discarded)
      return message

   def publish(self):
      session = self.show_session()
      #Check if current sessions has changes to commit.
      if session["changes"] > 0:
         req = self.api_call('publish')
      else:
         req = 'No changes to publish.'
      return req

   def logout(self):
      req = self.api_call('logout')
      req_message = "Logout:{m}".format(m=req["message"])
      return req_message

   #Firewall Policy
   def list_policies_packages(self):
      payload = { 'details-level':'full' }
      packages = self.api_call('show-packages',payload)
      self.package_policy = {}
      for p in packages["packages"]:
         key = p["name"]
         for a in p["access-layers"]:
            value = a["name"]
            self.package_policy[key] = value
      return self.package_policy
