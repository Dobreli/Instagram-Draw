from django.db import models
from django.db.models.deletion import CASCADE
from members.models import Member_Offers
from django.contrib.auth.models import User

class Bank(models.Model):
    id=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name = models.CharField(max_length=100,verbose_name='Alıcı Adı')
    bank_name=models.CharField(max_length=100,verbose_name='Banka adı')
    iban_no=models.CharField(max_length=26 ,verbose_name='Iban No')
    hesap_no=models.CharField(max_length=12 ,verbose_name='Hesap No',null=True,blank=True)
    branch_name=models.CharField(max_length=100 ,verbose_name='Şube adı',null=True,blank=True)
    branch_no=models.CharField(max_length=50 ,verbose_name='Şube No',null=True,blank=True)
    status=models.BooleanField(default='True',verbose_name='Banka Durumu')

    class Meta:
        verbose_name = "Bankalar"
        verbose_name_plural="Bankalar"
        
    def __str__(self):
        return str(self.bank_name)

class Payment_Type(models.Model):
    id=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    type_name = models.CharField(max_length=50,verbose_name='Ödeme Tipi')
    status=models.BooleanField(default='True',verbose_name='Durum')

    class Meta:
        verbose_name = "Ödeme Tipi"
        verbose_name_plural="Ödeme Tipi"
        
    def __str__(self):
        return str(self.type_name)

class Payment_Comment(models.Model):
    id=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    comment= models.CharField(max_length=100,verbose_name='İşlem Açıklama')
    status = models.BooleanField(default='True',verbose_name='Açıklama Durumu')
    class Meta:
        verbose_name = "Ödeme İşlem"
        verbose_name_plural="Ödeme İşlem"
        
    def __str__(self):
        return str(self.comment)

class Payment(models.Model):
    id=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    offer_id = models.ForeignKey(Member_Offers,on_delete=CASCADE,verbose_name='Ürün Teklif No')
    user_id = models.ForeignKey(User,on_delete=CASCADE,verbose_name="Kullanıcı")
    payment_type = models.ForeignKey(Payment_Type,on_delete=CASCADE,verbose_name="Ödeme Tipi")
    price = models.FloatField(verbose_name='Ödeme')
    date = models.DateTimeField(auto_created=True,auto_now_add=True, blank=True,verbose_name='Ödeme Tarihi')
    commentid = models.ForeignKey(Payment_Comment,on_delete=CASCADE,verbose_name="İşlem Açıklama")
    status = models.BooleanField(default='False',verbose_name='Ödeme Durumu')
    class Meta:
        verbose_name = "Ödemeler"
        verbose_name_plural="Ödemeler"
        
    def __str__(self):
        return str(self.id)


class Transfer_Comment(models.Model):
    id=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    comment= models.CharField(max_length=100,verbose_name='İşlem Açıklama')
    status = models.BooleanField(default='True',verbose_name='Açıklama Durumu')
    class Meta:
        verbose_name = "Havale İşlem"
        verbose_name_plural="Havale İşlem"
        
    def __str__(self):
        return str(self.comment)


class Payment_Transfer(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    payment_id = models.ForeignKey(Payment,on_delete=CASCADE,verbose_name='Ödeme No')
    bank_id = models.ForeignKey(Bank,on_delete=CASCADE, verbose_name='Banka')
    reference_no = models.CharField(max_length=100,verbose_name='Referans numarası')
    commentid = models.ForeignKey(Transfer_Comment,on_delete=CASCADE,verbose_name='İşlem Açıklama')
    check_status = models.BooleanField(default='False',verbose_name='Eksik Tutar Durumu')
    status = models.BooleanField(default='False',verbose_name="Havale Durumu")
    class Meta:
        verbose_name = "Havale/Eft"
        verbose_name_plural="Havale/Eft"
        
    def __str__(self):
        return str(self.id)



