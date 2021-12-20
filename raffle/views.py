import json
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
import random
from django.views.generic import View
from members.models import Members_Classes, User_Member_Class
from .models import Raffle, Raffle_Result
from django.contrib.auth.models import User
from django.contrib.humanize.templatetags.humanize import naturaltime
import os

def userform(userid):
    user_members = User_Member_Class.objects.filter(
        status=True, user_id=userid)

    if (len(user_members) == 0):
        return False
    else:
        member = []
        membername = []
        for mem in user_members:
            member.append(mem.member_id)

        for memid in member:
            m = Members_Classes.objects.get(name=str(memid))
            membername.append({'id': str(m.id), 'name': str(
                m.name), 'comment': str(m.coment_limit)})
        return membername


class ConvertList():
    import json

    def __init__(self, list):
        self.list = list

    def convert(self):
        if self.list != '':
            list_convert = str(self.list)
            check = "\/"
            for c in check:
                list_convert = list_convert.replace(c, "")
            list_convert = list_convert.replace("'", '"')
            list_dumps = json.dumps(list_convert)
            list_loads = json.loads(list_dumps)
            result = json.loads(list_loads)
            return result
        else:
            return ''


class Result:
    # coding=utf-8
    def __init__(self, mainlist, winner, backup, insta) -> None:
        self.winner = winner
        self.backup = backup
        self.list = mainlist
        self.backupnumber = self.backup
        self.winlist = []
        self.backuplist = []
        self.info = ''
        self.insta = insta

        self.checkwinner = []
        self.checkbackup = []

    def result(self):
        if self.backup != 0:

            self.number = len(self.list)-int(self.winner)

            if 0 < self.number < int(self.backup):
                self.backupnumber = self.number
                self.info = 'Liste sayısı az olduğundan yedek listesi kalan kullanıcılardan rasgele seçilerek sıralandı.'
                if self.insta == True:
                    Result.instaraffle(self)
                else:
                    Result.raffle(self)
                return {'winnerlist': self.winlist, 'backuplist': self.backuplist, 'info': self.info}

            elif self.number == 0:
                if self.insta == True:
                    Result.instaraffle(self)
                else:
                    Result.raffle(self)
                    self.info = 'Kazananlar ile liste eşit olduğundan yedek kişi seçilemedi.'
                return {'winnerlist': self.winlist, 'backuplist': self.backuplist, 'info': self.info}

            elif self.number < 0:
                self.info = 'Kazanan sayısı listedeki kişi sayısını geçemez.'
                return {'winnerlist': self.winlist, 'backuplist': self.backuplist, 'info': self.info}

            else:
                if self.insta == True:
                    Result.instaraffle(self)
                else:
                    Result.raffle(self)
                return {'winnerlist': self.winlist, 'backuplist': self.backuplist, 'info': self.info}

        else:
            if len(self.list) < int(self.winner):
                self.info = 'Kazanan sayısı listedeki kişi sayısını geçemez.'
                return {'winnerlist': self.winlist, 'backuplist': self.backuplist, 'info': self.info}
            else:
                if self.insta == True:
                    Result.instaraffle(self)
                else:
                    Result.raffle(self)
                return {'winnerlist': self.winlist, 'backuplist': self.backuplist, 'info': self.info}

    def raffle(self):
        for i in range(int(self.winner)):
            while True:
                user = random.choice(self.list)
                if user not in self.winlist:
                    self.winlist.append(user)
                    break

        if self.backup != 0:
            if self.backupnumber != self.backup:
                for i in range(int(self.backupnumber)):
                    while True:
                        user = random.choice(self.list)
                        if user not in self.winlist:
                            if user not in self.backuplist:
                                self.backuplist.append(user)
                                break

            elif self.backupnumber == self.backup:
                for i in range(int(self.backup)):
                    while True:
                        draw = random.choice(self.list)
                        if draw not in self.winlist:
                            if draw not in self.backuplist:
                                self.backuplist.append(draw)
                                break

    def instaraffle(self):
        for i in range(int(self.winner)):
            while True:
                user = random.choice(self.list)
                if user['userid'] not in self.checkwinner:
                    self.checkwinner.append(user['userid'])
                    self.winlist.append(user)
                    break

        if self.backup != 0:
            if self.backupnumber != self.backup:
                for i in range(int(self.backupnumber)):
                    while True:
                        user = random.choice(self.list)
                        if user['userid'] not in self.checkwinner:
                            if user['userid'] not in self.checkbackup:
                                self.checkbackup.append(user['userid'])
                                self.backuplist.append(user)
                                break

            elif self.backupnumber == self.backup:
                for i in range(int(self.backup)):
                    while True:
                        user = random.choice(self.list)
                        if user['userid'] not in self.checkwinner:
                            if user['userid'] not in self.checkbackup:
                                self.checkbackup.append(user['userid'])
                                self.backuplist.append(user)
                                break


class TextareaConvert:
    def __init__(self, text) -> None:
        self.text = str(text).split(',')
        self.newtext = []

    def convert(self):
        for follow in self.text:
            convert = str(follow).replace("\n", "")
            convert = convert.replace("\r", "")
            if convert != '':
                self.newtext.append(convert)
        return self.newtext


class FreeRaffle(View):
    def get(self, request):
        getraffle = Raffle.objects.filter(status = True).order_by('-id')[:4][::1]
        mainlist=[]
    
        for ge in getraffle:
            main = ConvertList(ge.main_user_list).convert()
            mainlist.append({'id':ge.id,'username':ge.username,'post_url':ge.post_url,'winner':ge.winner,'date':ge.date})
        raffle = Raffle.objects.all()
        totalcomment = 0
        totalwinner = 0

        for raf in raffle :
            totalcomment += len(ConvertList(raf.main_user_list).convert())
            totalwinner += raf.winner
        context = {
            'raffle':mainlist,
            'totalraffle':len(raffle),
            'totalcomment':totalcomment,
            'totalwinner':totalwinner,
        }
        return render(request, 'raffle/freeraffle.html',context=context)
        

    def post(self, request):
        self.title = request.POST.get('title')
        self.winner = request.POST.get('winner')
        self.raffle = request.POST.get('list')
        self.backup = request.POST.get('backup')
        self.raffle = TextareaConvert(self.raffle).convert()

        result = Result(winner=self.winner, mainlist=self.raffle,
                        backup=self.backup, insta=False).result()
        winnerlist = result['winnerlist']
        backuplist = result['backuplist']
        info = result['info']
        listlen = len(self.raffle)

        if request.is_ajax():
            return JsonResponse({'raffle_list': self.raffle, 'title': self.title, 'winner': winnerlist, 'backupwin': backuplist, 'info': info, 'len': listlen}, status=200)

        return render(request, 'raffle/freeraffle.html')


class TotalComment(View):
    def get(self, request):
        return redirect('index')

    def post(self, request):
        self.url = request.POST.get('posturl')
        self.username = request.POST.get('username')
        if request.is_ajax():
            try:
                import instaloader
                insta = instaloader.Instaloader()
                profile = instaloader.Profile.from_username(
                    insta.context, str(self.username))
                posts = profile.get_posts()
                for post in posts:
                    if post.shortcode in self.url:
                        comment = post.comments
                        break
                return JsonResponse({'totalcomment': comment}, status=200)
            except:
                comment = 'Hata! "Username" ya da "Gönderi Link" bilgilerini kontrol ediniz.'
                return JsonResponse({'totalcomment': comment}, status=200)
        if request.user.is_authenticated:
            current_user = request.user.id
            member = userform(current_user)
            if member == False:
                info = 'Bir Paket Satın Al'
                return render(request, 'raffle/instagramraffle.html', {'info': info})
            else:
                return render(request, 'raffle/instagramraffle.html', {'member': member})
        return render(request, 'raffle/instagramraffle.html')


class InstagramRaffle(View):
    def get(self, request):
        getraffle = Raffle.objects.filter(status=True).order_by('-id')[:4][::1]
        mainlist = []

        for get in getraffle:
            main = ConvertList(get.main_user_list).convert()
            mainlist.append({'id': get.id, 'username': get.username, 'post_url': get.post_url,
                             'winner': get.winner, 'date': get.date})
        raffle = Raffle.objects.all()
        totalcomment = 0
        totalwinner = 0

        for raf in raffle:
            totalcomment += len(ConvertList(raf.main_user_list).convert())
            totalwinner += raf.winner
        context = {
                    'raffle': mainlist,
                    'totalraffle': len(raffle),
                    'totalcomment': totalcomment,
                    'totalwinner': totalwinner,
                }
        if request.user.is_authenticated:
            current_user = request.user.id
            member = userform(current_user)
            if member == False:
                info = 'Bir Paket Satın Al'
                context = {
                    'raffle': mainlist,
                    'totalraffle': len(raffle),
                    'totalcomment': totalcomment,
                    'totalwinner': totalwinner,
                    'info':info
                }
                return render(request, 'raffle/instagramraffle.html', context=context)
            else:
                context = {
                        'raffle': mainlist,
                        'totalraffle': len(raffle),
                        'totalcomment': totalcomment,
                        'totalwinner': totalwinner,
                        'member':member,
                }
                return render(request, 'raffle/instagramraffle.html',context=context)
        return render(request, 'raffle/instagramraffle.html',context=context)

    def post(self, request):
        self.title = request.POST.get('title')
        self.username = request.POST.get('username')
        self.posturl = request.POST.get('posturl')
        self.member = request.POST.get('member')
        self.tag = request.POST.get('tag')
        self.followlist = request.POST.get('follow')
        self.textlist = request.POST.get('text')
        self.countuser = request.POST.get('useracount')
        self.backup = request.POST.get('backup')
        self.winner = request.POST.get('winner')
        self.animate = request.POST.get('animate')

        self.memberid = self.member.split("-")[0]
        self.membercomment = self.member.split(":")[2]
        self.current_user = request.user.id

        if self.countuser == 'Hayır':
            self.countuser = False
        else:
            self.countuser = True

        self.followlist = TextareaConvert(self.followlist).convert()
        self.textlist = TextareaConvert(self.textlist).convert()

        if self.followlist == []:
            self.followlist = ''

        if self.textlist == []:
            self.textlist = ''

        from app.InstaDraw import InstagramComment, DownloadProfilePicture,FollowCheck
        getcomment = InstagramComment(url=self.posturl, username=self.username,comment=self.membercomment,useracount=self.countuser,tag=self.tag,textlist=self.textlist,followlist=self.followlist).getcomment()
        validlist = getcomment['validlist']
        mainlist = getcomment['mainlist']
        if getcomment['ex'] == '':
            # Raffle
            result = Result(winner=self.winner, mainlist=validlist,backup=self.backup,insta=True).result()
            winner = result['winnerlist']
            backup = result['backuplist']
            info = result['info']
            if self.followlist != '':
                winner = FollowCheck(self.followlist,winner).followcheck()
                backup = FollowCheck(self.followlist,backup).followcheck()
            # Raffle databese upload
            user = User.objects.get(id=self.current_user)
            memberid = Members_Classes.objects.get(id=str(self.memberid))
            raffle = Raffle.objects.create(animate_time=self.animate, winner=self.winner,backup_winner=self.backup,user_id=user,member_id=memberid,title=self.title,post_url=self.posturl,username=self.username,count_a_user=self.countuser,tag= self.tag,text_list=self.textlist,follow_list=self.followlist,main_user_list=mainlist)
            raffle.save()
            # Raffle_Result databese upload
            # raffle_id= Raffle.objects.filter(post_url=self.posturl).last()
            # raffle = Raffle.objects.get(id=str(raffle_id)).id
            result = Raffle_Result.objects.create(raffle_id=raffle,winner_list=winner,backup_list=backup,valid_user_list=validlist)
            result.save()
            # result = Raffle_Result.objects.filter(raffle_id=raffle)
            # result = Raffle_Result.objects.get(id=str(result[0]))
            # User_Member remaining use update
            user_memberid = User_Member_Class.objects.filter(user_id=self.current_user, member_id= self.memberid)[0].id
            getntimes = User_Member_Class.objects.get(id=str(user_memberid))
            ntimes = int(getntimes.n_times)-1
            if ntimes ==0:
                getntimes.status = False
            getntimes.n_times = ntimes
            getntimes.save()
            path=os.getcwd()
            location = path+"\\static\\profilepic\\{}\\".format(raffle.id)
            DownloadProfilePicture(self.username, location=location).download()
            for usname in winner:
                DownloadProfilePicture(usname['username'], location=location).download()
            for usname in backup:
                DownloadProfilePicture(usname['username'], location=location).download()
            for flw in self.followlist :
                DownloadProfilePicture(flw, location=location).download()

            # if evriting is good
            if request.is_ajax():
                return JsonResponse({'winner': winner,'info':info,'raffleid':raffle.id,'status':True }, status=200)

        else:
            print(getcomment['ex'])
            winner = ''
            backup = ''
            info = ''
            if request.is_ajax():
                return JsonResponse({'winner': '','info':'','raffleid':'','status':False }, status=200)

        member = userform(self.current_user)
        if member == False:
            info = 'Bir Paket Satın Al'
            return render(request, 'raffle/instagramraffle.html', {'info':info})
        else:
            return render(request, 'raffle/instagramraffle.html', {'member':member})     


class InstagramRaffleResult(View):
    def get(self, request,raffleid):
        self.raffleid = raffleid
        self.raffle = Raffle.objects.get(id=str(self.raffleid))
        raffleid = self.raffle.id
        rafflepost = self.raffle.post_url
        raffletag = self.raffle.tag
        raffletext = ConvertList(self.raffle.text_list).convert()
        rafflefollow = ConvertList(self.raffle.follow_list).convert()
        raffleuser = self.raffle.user_id
        rafflecount = self.raffle.count_a_user
        return render(request, 'raffle/instagramraffleresult.html',{'count':rafflecount,'raffleid':raffleid,'raffleuser':str(raffleuser),'post':rafflepost,'tag':raffletag,'text':raffletext,'follow':rafflefollow})
    def post(self, request, raffleid):
        self.raffleid = raffleid
        self.raffle = Raffle.objects.get(id=str(self.raffleid))
        self.raffleresult = Raffle_Result.objects.filter(
            raffle_id=str(self.raffleid))[0].id
        self.raffleresult = Raffle_Result.objects.get(
            id=str(self.raffleresult))
        self.status = self.raffleresult.animate_status
        self.raffleresult.animate_status = False
        self.raffleresult.save()
        validlist = ConvertList(self.raffleresult.valid_user_list).convert()
        winner = ConvertList(self.raffleresult.winner_list).convert()
        backup = ConvertList(self.raffleresult.backup_list).convert()
        rafflefollow = ConvertList(self.raffle.follow_list).convert()
        
        title = self.raffle.title
        raffleid = self.raffle.id
        raffleuser = self.raffle.user_id
        
        if request.is_ajax():
            return JsonResponse({'animate': self.raffle.animate_time,'username':self.raffle.username,'url':self.raffle.post_url,'status':self.status,'winner':winner,'backup':backup,'validlist':validlist,'title':title,'follow':rafflefollow}, status=200)

        return render(request, 'raffle/instagramraffleresult.html',{'raffleid':raffleid,'raffleuser':raffleuser})


def reinstagramraffle(request):
    from app.InstaDraw import DownloadProfilePicture,FollowCheck
    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.is_ajax():
                raffleid = request.POST['raffleid']
                raffle = Raffle.objects.get(id=str(raffleid))
                raffleresult = Raffle_Result.objects.get(id=str(raffleid))
                mainlist = ConvertList(raffleresult.valid_user_list).convert()
                result = Result(winner=raffle.winner, mainlist=mainlist,backup=raffle.backup_winner,insta=True).result()
                winner = result['winnerlist']
                backup = result['backuplist']
                if raffle.follow_list != '':
                    winner = FollowCheck(raffle.follow_list,winner).followcheck()
                    backup = FollowCheck(raffle.follow_list,backup).followcheck()
                raffleresult.winner_list = winner
                raffleresult.backup_list = backup
                raffleresult.animate_status = True
                raffleresult.status = True
                raffle.status = True
                raffleresult.save()
                raffle.save()
                location = os.getcwd()+"\\static\\profilepic\\"+str(raffleid)+"\\"
                # location = 'C:/Users/DobreLi/Desktop/alpha/main/static/profilepic/'+ \
                #     str(raffleid)+'/'
                for usname in winner:
                    DownloadProfilePicture(usname['username'], location=location).download()
                for usname in backup:
                    DownloadProfilePicture(usname['username'], location=location).download()
                return JsonResponse({'info': True},status=200)
    else:
        return redirect('index')


def reference(request):
    getraffle = Raffle.objects.filter(status= True).order_by('-id')[:12][::1]
    mainlist = []

    for get in getraffle:
        main = ConvertList(get.main_user_list).convert()
        mainlist.append({'id': get.id,'username':get.username,'post_url':get.post_url,'winner':get.winner,'date':get.date})

    context = {
        'raffle': mainlist,
    }
    return render(request, 'raffle/reference.html', context=context)


class RaffleQuery(View):
    def get(self, request):
        return reference
    def post(self, request):
        self.raffleid = request.POST.get('raffleid')
        if request.is_ajax():
            raffle = Raffle.objects.filter(id=str(self.raffleid))
            mainlist = []
            if str(raffle) !='<QuerySet []>':
                for get in raffle:
                    main = ConvertList(get.main_user_list).convert()
                    mainlist.append({'id': get.id,'username':get.username,'post_url':get.post_url,'winner':get.winner,'date':naturaltime(get.date),'rafflestatus':get.status,'status':True})
                return JsonResponse(mainlist[0], status=200)
            else:
                mainlist.append({'status': False})
                return JsonResponse(mainlist[0], status=200)
        return reference
