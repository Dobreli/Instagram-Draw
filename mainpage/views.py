from django.shortcuts import redirect, render
import json
from raffle.models import Raffle

class ConvertList():
    import json
    def __init__(self,list):
        self.list = list
                
    def convert(self):
        list_convert = str(self.list)
        check = "\/"
        for c in check:
            list_convert = list_convert.replace(c,"")
        list_convert = list_convert.replace("'",'"')
        list_dumps= json.dumps(list_convert)
        list_loads=json.loads(list_dumps)
        result=json.loads(list_loads)
        return result

def index(request):
    getraffle = Raffle.objects.filter(status = True).order_by('-id')[:4][::1]
    mainlist=[]
    
    for get in getraffle:
        main = ConvertList(get.main_user_list).convert()
        mainlist.append({'id':get.id,'username':get.username,'post_url':get.post_url,'mainlist':len(main),'winner':get.winner,'date':get.date})
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
    }
    return render(request,'mainpage/index.html',context=context)


