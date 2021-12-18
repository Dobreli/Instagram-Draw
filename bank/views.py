from django.db import models
from django.shortcuts import redirect, render
from django.http.response import HttpResponse, JsonResponse
from members.models import Members_Classes,Member_Offers
from .models import Bank,Payment,Payment_Type,Payment_Transfer,Payment_Comment,Transfer_Comment
from django.contrib.auth.models import User
from django.views.generic import View
import json



class BuyMember(View):
    def post(self,request,id):
        if request.user.is_authenticated:
            if request.method == 'POST':
                if request.is_ajax():
                    datatype = request.POST['type']
                    data = json.loads(request.POST.get('data'))
                    if int(datatype)== 1:
                        cardusername =data['user']
                        cardno=data['cardno']
                        date=data['date'].split('/')
                        day=date[0]
                        month=date[1]
                        cvv= data['cvv']
                        return JsonResponse({'info':True},status=200)

                    if int(datatype) == 2:
                        referenceno=data['reference']
                        bankno=data['bank']
                        user=request.user.id
                        userid = User.objects.get(id=user)
                        offer = Member_Offers.objects.get(id=id).id
                        price = offer.price
                        paytype=Payment_Type.objects.get(id=datatype).id
                        commentid=Payment_Comment.objects.get(id=1).id
                        payment = Payment.objects.create(offer_id=offer,user_id=userid,payment_type=paytype,price=price,commentid=commentid)
                        payment.save()
                        bank = Bank.objects.get(id=bankno).id
                        commentid=Transfer_Comment.objects.get(id=1).id
                        transfer = Payment_Transfer.objects.create(payment_id=payment,bank_id=bank,reference_no=referenceno,commentid=commentid)
                        transfer.save()

                        return JsonResponse({'info':True},status=200)

            return HttpResponse('bank/buymember.html')
        else:
            return redirect('members')
    def get(self,request,id):
        offer_id = id
        offer = Member_Offers.objects.get(id=offer_id)
        memberid = offer.member_id
        price = offer.price
        ntimes = offer.n_times
        member = Members_Classes.objects.get(name=str(memberid))
        name = member.name
        limit = member.coment_limit

        bank = Bank.objects.all()

        context={
            'memberid':memberid,
            'price':price,
            'ntimes':ntimes,
            'name':name,
            'limit':limit,
            'bank':bank,
            'id':id

            }
        return render(request ,'bank/buymember.html',context=context)
    




def paymenttransfer(request,id):
    pass

def paymentcredit(request,id):
    pass