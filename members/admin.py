from django.contrib import admin
from .models import Members_Classes,Member_Offers,User_Member_Class

class CustomMemberClasses(admin.ModelAdmin):
    list_display=('id','name','content','coment_limit','tag_permission','follow_permission','text_permission','status')
admin.site.register(Members_Classes,CustomMemberClasses)
class CustomMemberOffers(admin.ModelAdmin):
    list_display=('id','member_id','n_times','price','status')
admin.site.register(Member_Offers,CustomMemberOffers)
class CustomUserMemberClass(admin.ModelAdmin):
    list_display=('id','user_id','member_id','n_times','status')
admin.site.register(User_Member_Class,CustomUserMemberClass)