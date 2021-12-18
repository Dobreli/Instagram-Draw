from django.db import models
from django.contrib.auth.models import User

class Members_Classes(models.Model):
    id=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name=models.CharField(max_length=50,verbose_name='Üyelik Adı')
    content=models.TextField(max_length=300,verbose_name='Açıklama')
    coment_limit=models.IntegerField(verbose_name='Çekilecek Yorum Limiti')
    tag_permission=models.BooleanField(default=False,verbose_name='Etiket İzni')
    follow_permission=models.BooleanField(default=False,verbose_name='Takip İzni')
    text_permission=models.BooleanField(default=False,verbose_name='Yazı Kontrol İzni')
    status=models.BooleanField(default=True,verbose_name='Durum')

    class Meta:
        verbose_name = "Üyelik Sınıfları"
        verbose_name_plural="Üyelik Sınıfları"

    def __str__(self) -> str:
        return str(self.name)

class Member_Offers(models.Model):
    id=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    member_id=models.ForeignKey(Members_Classes,on_delete=models.CASCADE,verbose_name='Member Id')
    n_times=models.IntegerField(verbose_name='Adet')
    price=models.FloatField(verbose_name='Fiyat')
    status=models.BooleanField(default=True,verbose_name='Durum')

    class Meta:
        verbose_name = "Üyelik Sınıf Teklifleri"
        verbose_name_plural="Üyelik Sınıf Teklifleri"
        
    def __str__(self) -> str:
        return str(self.id)

class User_Member_Class(models.Model):
    id=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    user_id=models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='User Id')
    member_id=models.ForeignKey(Members_Classes,on_delete=models.CASCADE,verbose_name='Üyelik Sınıf Id')
    n_times=models.IntegerField(verbose_name='Kalan Hakkı')
    status=models.BooleanField(default='False',verbose_name='Sınıf Durumu')

    class Meta:
        verbose_name = "Kullanıcı Üye Sınıf Bilgileri"
        verbose_name_plural="Kullanıcı Üye Sınıf Bilgiler"
        
    def __str__(self):
        return str(self.id)




