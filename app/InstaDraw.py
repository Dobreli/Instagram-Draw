from io import RawIOBase
import instaloader
from instagram_private_api import Client
import json
import codecs
import os
import datetime
import requests

class Login:
    class UpdateSettings:
        def __init__(self,path=r"app\cookie\settings.json"):
            self.path = path

        def readsettings(self):
            with open(self.path) as f:
                data = json.load(f)
                return data

        def writesettings(self,username, password, date, path):
            data ={}
            data.update(Login.UpdateSettings().readsettings())
           
            with open(self.path, "w") as f:
                new = {username: {"password": password,
                                "lastlogin": date, "cookiepath": path}}
                data.update(new)
                json.dump(data, f)

    class LoginDateCheck:
        def __init__(self, username):
            self.username = username
            self.settings = {}
            

        def checkdate(self):  
            self.settings.update(Login.UpdateSettings().readsettings())  
            now = datetime.datetime.now()
            logindate = self.settings[self.username]["lastlogin"]
            date = now-datetime.datetime.fromisoformat(logindate)
            if date.days > 30:
                return False
            else:
                return True
    
    class ApiLogin:
        def __init__(self) -> None:
            self.username =""
            self.password = ""
            self.lasdate = ""
            self.cookiepath = ""
            self.path = "app\\cookie"

        def getuser(self):
            data = Login.UpdateSettings().readsettings()
            for d in data:
                self.username = d
                break
            self.password = data[self.username]["password"]
            self.lasdate = data[self.username]["lastlogin"]
            self.cookiepath = data[self.username]["cookiepath"]
        def from_json(self,json_object):
            if '__class__' in json_object and json_object['__class__'] == 'bytes':
                return codecs.decode(json_object['__value__'].encode(), 'base64')
            return json_object

        def login(self):
            Login.ApiLogin.getuser(self)
            if Login.LoginDateCheck(self.username).checkdate() == False:
                os.chdir(self.path)
                if os.path.exists(self.username+".json"):
                    os.remove(self.username+".json")
                os.chdir("..")
                os.chdir("..")
                print(os.listdir())
                print(os.getcwd())
                self.cookiepath = os.path.join("{}\\{}.json".format(self.path,self.username))
                print(self.cookiepath)
                os.system("python app\\loginjson.py  -u {} -p {} -settings {}".format(self.username,self.password,self.cookiepath))
                Login.UpdateSettings().writesettings(username=self.username,password=self.password,date=str(datetime.datetime.now()),path=self.cookiepath )
                
            
            with open(self.cookiepath) as file_data:
                cached_settings = json.load(file_data, object_hook=Login.ApiLogin().from_json)    
                api=Client(self.username,self.password,settings=cached_settings)
            return api

class DownloadProfilePicture:
    def __init__(self, username, location) -> None:
        self.location = location
        self.username = username

    def download(self):
        insta = instaloader.Instaloader()
        profile = instaloader.Profile.from_username(
            insta.context, self.username)
        # download_title_pic dirname1 = Path
        user = insta.download_profilepic(profile, location=self.location)

class FollowCheck:
    def __init__(self,followlist,checklist) -> None:
        self.followlist = followlist
        self.checklist = checklist
        self.followlistid = GetId(self.followlist).getid()

    def followcheck(self):
        self.checkuserid = []
        for coment in self.checklist:
            for follow in self.followlistid:
                checkfollow =Login.ApiLogin().login().user_followers(int(follow),rank_token=Login.ApiLogin().login().generate_uuid(),query=coment["username"])
                if len(checkfollow['users'])>0:
                    coment[self.followlist[self.followlistid.index(follow)]]='True'
                else:
                    coment[self.followlist[self.followlistid.index(follow)]]='False'
        return self.checklist

class GetId:
    def __init__(self,followlist) -> None:
        self.followlist = followlist
        self.n_followlist = []
    
    def getid(self):
        insta = instaloader.Instaloader()
        for follow in self.followlist:
            profile = instaloader.Profile.from_username(insta.context, str(follow))
            self.n_followlist.append(profile.userid)
        return self.n_followlist

class Find_Media_Id:
    """
        Docstring:  if instagram api get comments, need 'media id'
        input: url = İnstagram Media link
        output: media_id 
    """
    def __init__(self,url) -> None:
        self.mediaurl=url

    def findid(self):
        try:
            html = requests.get("http://api.instagram.com/oembed?url={}".format(self.mediaurl)).content
            media_json = json.loads(html.decode('utf-8'))
            media_id=media_json["media_id"]
            return {'media_id': media_id, 'ex': ''}
        except Exception as ex:
            return {'media_id': '', 'ex': f'Find id hatasi : {ex}'}

class FindMediaId:

    """
        Docstring:  if instagram api get comments, need 'media id'

        input:
            url = İnstagram Media link
            username = Media owner username
        output:
            media_id and media_user_id(owner)
    """

    def __init__(self, url, username):
        self.url = url
        self.username = username

    def findid(self):
        try:
            insta = instaloader.Instaloader()
            profile = instaloader.Profile.from_username(
                insta.context, str(self.username))
            posts = profile.get_posts()
            for post in posts:
                if post.shortcode in self.url:
                    media_id = str(post.mediaid)+"_"+str(post.owner_id)
                    media_user_id = post.owner_id
                    return {'media_user_id': media_user_id, 'media_id': media_id, 'ex': ''}

            return {'media_user_id': '', 'media_id': '', 'ex': 'HATA! - Find id : Username ya da post url yanliş'}

        except Exception as ex:
            return {'media_user_id': '', 'media_id': '', 'ex': f'Find id hatasi : {ex}'}

class InstagramApi:
    """
        Docstring: Get all user comment

        input:
            media_id = int | Media id.
            comment = int | Get number of comments
            useracount = Bool | Each user is counted once. İf value False, adds all user.
        output:
            global all_userlist
    """

    def __init__(self, media_id, comment, useracount, username):
        self.media_id = media_id
        self.comment = comment
        self.useracount = useracount
        self.username = username
        self.main_userlist = []
        self.check = []

    def getcomment(self):
            try:
                api =Login.ApiLogin().login()
                self.comments = api.media_n_comments(
                    media_id=self.media_id, n=int(self.comment), reverse=True)
                for comment in self.comments:
                    self.get_userid = comment["user_id"]
                    self.get_usercomment = comment["text"]
                    self.get_username = comment["user"]["username"]
                    self.get_userfullname = comment["user"]["full_name"]

                    fullname = str(self.get_userfullname).replace('"', "")
                    coment = str(self.get_usercomment).replace('"', "")
                    coment = coment.replace('\n', "")
                    coment = coment.replace('\r', "")
                    coment = coment.replace('[', "")
                    coment = coment.replace(']', "")

                    check = "'?’,:;?\}$][(#){/&%+¿^!~"
                    for c in check:
                        nfullname = fullname.replace(c, "")
                        ncomment = coment.replace(c, "")
                        coment = ncomment
                        fullname = nfullname

                    self.get_userfullname = fullname
                    self.get_usercomment = coment
                    InstagramApi.addcomment(self)

                return {'main_list': self.main_userlist, 'ex': ''}
            except Exception as ex:
                return {'main_list':'','ex':f'HATA ! Api -{ex}'}

    def addcomment(self):
        if self.useracount == True:
            if self.get_username != self.username:
                if self.get_username not in self.check:
                    self.check.append(self.get_username)
                    self.main_userlist.append({"userid": self.get_userid, "username": self.get_username, "userfullname": self.get_userfullname, "usercoment": self.get_usercomment})
        else:
            if self.get_username != self.username:
                self.main_userlist.append({"userid": self.get_userid, "username": self.get_username,"userfullname": self.get_userfullname, "usercoment": self.get_usercomment})

class InstagramCheck:
    """
        Docstring: Conditional comment control

        input: 

            tag = int | Check hastag counts.
            followlist = list | username to follow list
            textlist = list | comment have texts
            flolow = bool | follow control status
            
        output:
            ft_alluserlist
    """
    def __init__(self,mainuserlist,tag,textlist):
        self.textlist=textlist
        self.tag=tag
        self.followlist=[]
        self.followlistid=[]
        self.mainuserlist=mainuserlist

        self.validuserlist=[] # = Valid
        self.txt_alluserlist=[] # = text
        self.t_alluserlist=[] # t = tag

    
    def checkreturn(self):

        if len(self.textlist)>0 and int(self.tag)>0:
            InstagramCheck.tagcheck(self,self.mainuserlist)
            self.validuserlist = self.t_alluserlist
            InstagramCheck.textcheck(self,self.validuserlist)
            self.validuserlist = self.txt_alluserlist
            return self.validuserlist

        elif len(self.textlist)==0 and int(self.tag)>0:
            InstagramCheck.tagcheck(self,self.mainuserlist)
            self.validuserlist = self.t_alluserlist
            return self.validuserlist

        elif len(self.textlist)>0 and int(self.tag)==0:
            InstagramCheck.textcheck(self,self.mainuserlist)
            self.validuserlist = self.txt_alluserlist
            return self.validuserlist

        elif len(self.textlist)==0 and int(self.tag)==0:
            self.validuserlist = self.mainuserlist
            return self.validuserlist

    def textcheck(self,list):
        if len(self.textlist)>0:
            for coment in list:
                a = 0
                num = len(self.textlist)
                for text in self.textlist:
                    if text.lower() in str(coment['usercoment']).lower():
                        print(coment['usercoment'])
                        print('buldu : ',text)
                        a+=1
                if a == num :
                    self.txt_alluserlist.append(coment)

    def tagcheck(self,list):
        if int(self.tag)>0:
           for coment in list:
               if str(coment['usercoment']).count('@') == int(self.tag):
                    self.t_alluserlist.append(coment)
                # coment['usercoment']=str(coment['usercoment']).count('@')
                # self.t_alluserlist.append(coment)
    
class InstagramComment:
    def __init__(self,url,username,comment, useracount,tag,textlist,followlist) -> None:
        self.url = url
        self.username = username
        self.comment = comment
        self.useracount = useracount
        self.tag = tag
        self.textlist = textlist
        self.followlist = followlist

    def getcomment(self):
        try:
            mediaid= FindMediaId(url=self.url,username=self.username).findid()
        except:
            mediaid= Find_Media_Id(url=self.url).findid()

        if mediaid['ex'] == '':
            mediaid=mediaid['media_id']
            api = InstagramApi(media_id=mediaid,comment=self.comment,useracount=self.useracount,username=self.username).getcomment()
            if api['ex'] == '':
                check = InstagramCheck(mainuserlist=api['main_list'],tag=self.tag,textlist=self.textlist).checkreturn()
                return {'mainlist':api['main_list'],'validlist':check,'ex':''}
            else:
                return {'mainlist':'','validlist':'','ex':api['ex']}
        else:
            return {'mainlist':'','validlist':'','ex':mediaid['ex']}



# def getid(user):
#     insta = instaloader.Instaloader()
#     userid = instaloader.Profile.from_username(insta.context, str(user)).userid
#     return userid
# followers = Login.ApiLogin().login().user_followers(int(getid("dobreli01")),rank_token=Login.ApiLogin().login().generate_uuid(),max_id=140)
# following = Login.ApiLogin().login().user_following(int(getid("dobreli01")),rank_token=Login.ApiLogin().login().generate_uuid(),max_id=140)

# def convert(dict):
#     follow=[]
#     dict=dict["users"]
#     for i in dict:
#         follow.append(i["username"])
#     return follow

