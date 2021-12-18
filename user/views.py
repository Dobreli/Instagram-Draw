import json
from math import inf
import re
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages
from django import forms
from members.models import Members_Classes, User_Member_Class,Member_Offers
from raffle.models import Raffle
from bank.models import Payment, Payment_Comment,Payment_Transfer,Payment_Type,Bank, Transfer_Comment
from django.contrib.humanize.templatetags.humanize import naturaltime

class ConvertList():
    import json

    def __init__(self, list):
        self.list = list

    def convert(self):
        list_convert = str(self.list)
        check = "\/"
        for c in check:
            list_convert = list_convert.replace(c, "")
        list_convert = list_convert.replace("'", '"')
        list_dumps = json.dumps(list_convert)
        list_loads = json.loads(list_dumps)
        result = json.loads(list_loads)
        return result


class registerform(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()


def login(request):
    if request.method == 'POST':
        if request.is_ajax():
            username = request.POST["login-username"]
            password = request.POST["login-password"]
            user = auth.authenticate(username=username, password=password)

            if user is not None:
                auth.login(request, user)
                return JsonResponse({'status': True})
            else:
                return JsonResponse({'status': False})
        else:
            username = request.POST["username"]
            password = request.POST["password"]
            user = auth.authenticate(username=username, password=password)

            if user is not None:
                auth.login(request, user)
                messages.add_message(request, messages.SUCCESS,
                                     'Hoşgeldiniz : '+username)
                return redirect('index')
            else:
                messages.add_message(
                    request, messages.ERROR, 'Giriş yapılamadı. Username ve Şifre bilgilerinden biri yanlış !')
                return redirect('login')

    else:
        if request.user.is_authenticated:
            return redirect('index')
        else:
            return render(request, "user/login.html")


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.add_message(request, messages.SUCCESS,
                             'Oturumunuz kapatıldı.')
        return redirect('login')
    else:
        return redirect('index')


def check_password(psw):
    import re
    if len(psw) < 8:
        raise Exception("En az 8 karakter içerelidir")
    elif not re.search("[a-z]", psw):
        raise Exception(
            "Parola küçük harf içermelidir")
    elif not re.search("[A-Z]", psw):
        raise Exception(
            "Parola büyük harf içermelidir.")


def register(request):
    form = registerform(request.POST or None)
    if request.method == 'POST':
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        repassword = request.POST["repassword"]
        if User.objects.filter(username=username).exists():
            messages.add_message(
                request, messages.WARNING, username+': Bu kullanıcı adı daha önce alınmış !')
            return render(request, "user/register.html", {'form': form})

        else:
            if str(username).isalnum():
                if User.objects.filter(email=email).exists():
                    messages.add_message(
                        request, messages.WARNING, email+': Bu mail adresi daha önce alınmış !')
                    return render(request, "user/register.html", {'form': form})
                else:
                    if password == repassword:
                        try:
                            check_password(password)
                            user = User.objects.create_user(
                                username=username, email=email, password=password)
                            user.save()
                            us = auth.authenticate(
                                username=username, password=password)
                            auth.login(request, us)
                            userid = request.user.id
                            userid = User.objects.get(id=userid)
                            members = Members_Classes.objects.all()
                            for member in members:
                                memberid = Members_Classes.objects.get(
                                    id=str(member.id))
                                if str(member.id) == '1':
                                    usermember = User_Member_Class.objects.create(
                                        user_id=userid, member_id=memberid, n_times=1)
                                else:
                                    usermember = User_Member_Class.objects.create(
                                        user_id=userid, member_id=memberid, n_times=0)
                                usermember.save()
                            messages.add_message(
                                request, messages.SUCCESS, 'Hoşgeldiniz : '+username)
                            return redirect('index')
                        except Exception as e:
                            messages.add_message(
                                request, messages.WARNING, 'Şifre Kurallara Uymuyor - '+str(e))
                            return render(request, "user/register.html", {'form': form})
                    else:
                        messages.add_message(
                            request, messages.WARNING, 'Şifreler uyuşmuyor !')
                        return render(request, "user/register.html", {'form': form})
            else:
                messages.add_message(
                    request, messages.WARNING, 'Kullanıcı adı harflerden ve rakamlardan oluşmalıdır.')
                return render(request, "user/register.html", {'form': form})

    else:
        if request.user.is_authenticated:
            return redirect('index')
        else:
            return render(request, "user/register.html")


def buyregister(request):         
    if request.method == 'POST':
        link=request.POST["link"]
        if request.is_ajax():
            def checkpassword(psw):
                import re
                info = ''
                if len(psw) < 8:
                    info ="En az 8 karakter içerelidir"
                    return info
                elif not re.search("[a-z]", psw):
                    info ="Parola küçük harf içermelidir"
                    return info       
                elif not re.search("[A-Z]", psw):
                    info ="Parola en az bir büyük harf içermelidir."
                    return info
                else:
                    info = True
                    return info
            username = request.POST["username"]
            email = request.POST["email"]
            password = request.POST["password"]
            repassword = request.POST["repassword"]
            if User.objects.filter(username=username).exists():
                return JsonResponse({'status': False, 'info': 'Bu ' + '"' + username + '"' + ' kullanıcı adı alınmış.', 'no': 1})
            else:
                if str(username).isalnum():
                    if User.objects.filter(email=email).exists():
                        return JsonResponse({'status': False, 'info': 'Bu emeil adresi ile kayıt olunmuş!', 'no': 2})
                    else:
                        if password == repassword:
                            chk = checkpassword(password)
                            if chk == True:
                                user = User.objects.create_user(username=username, email=email, password=password)
                                user.save()
                                us = auth.authenticate(username=username, password=password)
                                auth.login(request, us)
                                userid = request.user.id
                                userid = User.objects.get(id=userid)
                                members = Members_Classes.objects.all()
                                for member in members:
                                    memberid = Members_Classes.objects.get(
                                        id=str(member.id))
                                    if str(member.id) == '1':
                                        usermember = User_Member_Class.objects.create(
                                            user_id=userid, member_id=memberid, n_times=1)
                                    else:
                                        usermember = User_Member_Class.objects.create(
                                            user_id=userid, member_id=memberid, n_times=0)
                                    usermember.save()
                                return JsonResponse({'status': True})
                            else:
                                
                                return JsonResponse({'status': False, 'info': chk, 'no': 3})
                else:
                    return JsonResponse({'status': False, 'info': 'Kullanıcı adı harflerden ve rakamlardan oluşmalıdır.', 'no': 4})
        return HttpResponse(link)



def checkusername(request):
    if request.method == 'POST':
        if request.is_ajax():
            username = request.POST.get("username")
            if User.objects.filter(username=username).exists():
                return JsonResponse({'status': False, 'no': 1})
            else:
                if str(username).isalnum():
                    return JsonResponse({'status': True})
                else:
                    return JsonResponse({'status': False, 'no': 2})


def profile(request, username):
    if request.user.is_authenticated:
        if request.method == 'GET':
            return render(request, 'user/profile.html')

        if request.method == 'POST':
            firstname = request.POST['first_name']
            lastname = request.POST['last_name']
            userid = request.user.id
            user = User.objects.get(id=userid)
            user.first_name = firstname
            user.last_name = lastname
            user.save()
            if request.is_ajax():
                return JsonResponse({'info': True}, status=200)
            return render(request, 'user/profile.html')
    else:
        return redirect('index')


def userraffle(request, username):
    if request.user.is_authenticated:
        if request.method == 'GET':
            userid = request.user.id
            getraffle = Raffle.objects.filter(
                user_id=userid).order_by('-id')[:6][::1]
            mainlist = []
            for get in getraffle:
                main = ConvertList(get.main_user_list).convert()
                mainlist.append({'id': get.id, 'username': get.username, 'post_url': get.post_url, 'mainlist': len(
                    main), 'winner': get.winner, 'date': get.date, 'durum': get.status})
            if mainlist == []:
                mainlist = ''
            context = {
                'raffle': mainlist,
            }
            return render(request, 'user/userraffle.html', context=context)
        if request.method == 'POST':
            if request.is_ajax():
                postid = request.POST['no']
                raffle = Raffle.objects.get(id=postid)
                stat = raffle.status
                if stat == True:
                    raffle.status = False
                else:
                    raffle.status = True
                raffle.save()
                stat = raffle.status

                return JsonResponse({'info': stat}, status=200)

    else:
        return redirect('index')


def usermoreraffle(request, username):
    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.is_ajax():
                resultlen = int(request.POST['resultlen'])
                userid = request.user.id
                check = Raffle.objects.filter(user_id=userid)
                mainlist = []
                if len(check) > resultlen:
                    getraffle = Raffle.objects.filter(user_id=userid).order_by(
                        '-id')[resultlen:resultlen+6][::1]
                    for get in getraffle:
                        main = ConvertList(get.main_user_list).convert()
                        date = naturaltime(get.date)
                        mainlist.append({'id': get.id, 'username': get.username, 'post_url': get.post_url, 'mainlist': len(
                            main), 'winner': get.winner, 'date': date, 'status': get.status})
                    addstatus = True
                else:
                    addstatus = False

                return JsonResponse({'info': mainlist, 'add_status': addstatus}, status=200)
    else:
        return redirect('index')


def usermembers(request, username):
    if request.user.is_authenticated:
        userid = User.objects.get(id=request.user.id)
        members = Members_Classes.objects.all()
        usermember = User_Member_Class.objects.filter(user_id=userid)
        usermemberlist = []
        for memb in members:
            for usermem in usermember:
                if usermem.member_id == memb:
                    n = {'id': memb.id, 'name': memb.name, 'n': usermem.n_times}
                    if n not in usermemberlist:
                        usermemberlist.append(n)
                        
        memberlist=[]
        for i in members:
            if i.status == True:
                getprice = Member_Offers.objects.filter(member_id=str(i.id))[0]
                memberlist.append({'name':i.name,'content':i.content,'comentlimit':i.coment_limit,'tag':i.tag_permission,'follow':i.follow_permission,'text':i.text_permission,'price':getprice.price,'offers_id':getprice.id})
        return render(request, 'user/usermembers.html', context={'usermembers': usermemberlist,'members':memberlist})
    else:
        return redirect('index')


def userbuy(request, username):
    user =User.objects.get(id = str(request.user.id))
    payment = Payment.objects.filter(user_id=user)#.order_by('-id')[:6][::1]
    paymentlist =[]
    for pay in payment:
        payno=pay.id
        offer = Member_Offers.objects.get(id=str(pay.offer_id))
        member = Members_Classes.objects.get(name=str(offer.member_id)).name
        paytype=Payment_Type.objects.get(type_name=str(pay.payment_type)).type_name
        price = pay.price
        date = pay.date
        status = pay.status
        comment = pay.commentid
        comment = Payment_Comment.objects.get(comment = str(comment)).comment
        paymentlist.append({'payno':payno,'member':member,'paytype':paytype,'price':price,'date':date,'comment':comment,'status':status})
    transferlist =[]
    paytransfer = Payment.objects.filter(payment_type=2,user_id=user)
    for paytra in paytransfer:
        transfer = Payment_Transfer.objects.filter(payment_id=paytra.id)
        for tra in transfer:
            bank = Bank.objects.get(bank_name=str(tra.bank_id)).bank_name
            comment = Transfer_Comment.objects.get(comment=str(tra.commentid)).comment
            transferlist.append({'paymentno':paytra.id,'transferno':tra.id,'bank':bank,'reference':tra.reference_no,'comment':comment,'check_status':tra.check_status,'status':tra.status})

    context ={
        'payment':paymentlist,
        'transfer':transferlist,
    } 
    return render(request, 'user/userbuy.html',context=context)


def settings(request, username):
    return render(request, 'user/settings.html')


def changepassword(request, username):
    if request.method == 'POST':
        if request.is_ajax():
            oldpassword=request.POST['oldpassword']
            npassword=request.POST['npassword']
            renpassword=request.POST['renpassword']
            user = auth.authenticate(username=username, password=oldpassword)
            if user is not None:
                if npassword !=oldpassword:
                    if npassword == renpassword:
                        def checkpassword(psw):
                            import re
                            info = ''
                            if len(psw) < 8:
                                info ="En az 8 karakter içerelidir"
                                return info
                            elif not re.search("[a-z]", psw):
                                info ="Parola küçük harf içermelidir"
                                return info       
                            elif not re.search("[A-Z]", psw):
                                info ="Parola en az bir büyük harf içermelidir."
                                return info
                            else:
                                info = True
                                return info
                        psw = checkpassword(npassword)
                        if psw == True:
                            us = User.objects.get(username=username)
                            us.set_password(npassword)
                            us.save()
                            return JsonResponse({'info': True}, status=200)
                        else:
                            return JsonResponse({'info': False,'danger':2,'dangerinfo':psw}, status=200)
                    else:
                        return JsonResponse({'info': False,'danger':3}, status=200)
                else:
                    return JsonResponse({'info': False,'danger':4}, status=200)
            else:
                return JsonResponse({'info': False,'danger':1}, status=200)

    return render(request, 'user/profile.html')

def changemail(request, username):
    if request.method == 'POST':
        if request.is_ajax():
            password = request.POST['password']
            email = request.POST['email']
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                if User.objects.filter(email=email).exists():
                    return JsonResponse({'info': False,'danger':2}, status=200)
                else:
                    user= User.objects.get(username=username)
                    user.email=email
                    user.save()
                    return JsonResponse({'info': True}, status=200)
            else:
                return JsonResponse({'info': False,'danger':1}, status=200)
    return render(request, 'user/profile.html')
