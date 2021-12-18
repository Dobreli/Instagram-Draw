from django.contrib import admin
from .models import Bank, Payment_Comment,Payment_Type,Payment,Payment_Transfer,Transfer_Comment

class CustomBank(admin.ModelAdmin):
    list_display  = ('id','bank_name','iban_no','status')
    list_display_links =('id','bank_name','iban_no')
    search_fields  = ("bank_name",)
    # list_editable=
admin.site.register(Bank,CustomBank)

class CustomPayment(admin.ModelAdmin):
    list_display  = ('id','offer_id','user_id','payment_type','price','date','commentid','status')
    search_fields  = ("user_id","id")
    
admin.site.register(Payment,CustomPayment)

class CustomPaymentTransfer(admin.ModelAdmin):
    list_display  =('id','payment_id','bank_id','reference_no','commentid','check_status','status')
    search_fields  = ("payment_id","id")
admin.site.register(Payment_Transfer,CustomPaymentTransfer)

class CustomPaymentType(admin.ModelAdmin):
    list_display  =('id','type_name','status')
admin.site.register(Payment_Type,CustomPaymentType)

admin.site.register(Payment_Comment)
admin.site.register(Transfer_Comment)

