import json
import requests

class Check_Point(object):
   def __init__(self,host,port,username,password):
      self.host = host
      self.port = port
      self.username = username
      self.password = password
      self.url_base = "{h}:{p}/web_api"



                             
