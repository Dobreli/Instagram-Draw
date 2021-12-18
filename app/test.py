from logging import log
from instagram_private_api import Client
import codecs
import instaloader
import os
import json
import datetime
import requests
import ast
from InstaDraw import InstagramComment



# api = Login().ApiLogin().login()
url="https://www.instagram.com/p/CXVzMqtMpT0/?utm_source=ig_web_copy_link"
# media_id = Find_Media_Id(url).findid()
# InstagramApi(media_id=media_id["media_id"],comment=350,useracount=True,username="donanimarşivi").getcomment()



print(InstagramComment(url,"donanimarsivi",150,True,0,"","donanimarsivi").getcomment())