from django.shortcuts import render
from .models import Members_Classes,Member_Offers
from raffle.models import Raffle
import json
# Create your views here.
class ConvertList():
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
def members(request):
    get= Members_Classes.objects.all()
    memberlist=[]
    for i in get:
        if i.status == True:
            getprice = Member_Offers.objects.filter(member_id=str(i.id))[0]
            memberlist.append({'name':i.name,'content':i.content,'comentlimit':i.coment_limit,'tag':i.tag_permission,'follow':i.follow_permission,'text':i.text_permission,'price':getprice.price,'offers_id':getprice.id})

    getraffle = Raffle.objects.filter(status = True).order_by('-id')[:4][::1]
    mainlist=[]
    
    for ge in getraffle:
        main = ConvertList(ge.main_user_list).convert()
        mainlist.append({'id':ge.id,'username':ge.username,'post_url':ge.post_url,'mainlist':len(main),'winner':ge.winner,'date':ge.date})
    raffle = Raffle.objects.all()
    totalcomment = 0
    totalwinner = 0

    for raf in raffle :
        totalcomment += len(ConvertList(raf.main_user_list).convert())
        totalwinner += raf.winner
    context = {
            'raffle':mainlist,
            'totalraffle':len(raffle),
            'totalwinner':totalwinner,
            'member':memberlist,
        }       
    return render(request,'members/members.html',context)


