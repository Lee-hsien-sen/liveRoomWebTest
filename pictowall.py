import requests
from sign import addSign
import json
class pictowall():
    def postpictowall(self,live_id,user_id,group_id,picwall_id,img_url):
        url="http://10.200.241.12:8201/i/live/small-class/photo-wall/upload-callback"
        dic={}
        dic["live_id"]=live_id
        # requests.post(url,data=)
        #该方案需学生连接websocket暂时废弃