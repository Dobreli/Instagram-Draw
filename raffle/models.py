from django.db import models
from django.contrib.auth.models import User
from members.models import Members_Classes

class Raffle(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    user_id = models.ForeignKey(User,on_delete=models.CASCADE, verbose_name='User_id')
    member_id = models.ForeignKey(Members_Classes,on_delete=models.CASCADE, verbose_name='Member_id')
    title = models.CharField(max_length=100,serialize=False, verbose_name='Başlık')
    post_url = models.URLField(verbose_name="Post url")
    username = models.CharField(max_length=100, verbose_name="Username")
    count_a_user = models.BooleanField(verbose_name='Kullanıcı bir kere sayılsın')
    tag = models.IntegerField(verbose_name='Etiket Sayısı')
    text_list = models.TextField(null=True,verbose_name='Yorumda olması gereken yazılar')
    follow_list = models.TextField(null=True,verbose_name='Takip etmesi gerekenler')
    main_user_list = models.TextField(verbose_name='Tüm yapılan yorumlar')
    winner = models.IntegerField(verbose_name='Kazanan Sayısı')
    backup_winner = models.IntegerField(verbose_name='Yedek Sayısı')
    animate_time = models.IntegerField(verbose_name='Animasyon süresi')
    date = models.DateTimeField(auto_now_add=True, blank=True)
    status = models.BooleanField(default=True,verbose_name='Durum')

    def __str__(self) -> str:
        return str(self.username)

class Raffle_Result(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    raffle_id = models.ForeignKey(Raffle,on_delete=models.CASCADE,verbose_name='Çekiliş Numarası')
    winner_list = models.TextField(verbose_name='Kazanan listesi')
    backup_list = models.TextField(verbose_name='Yedek listesi')
    valid_user_list = models.TextField(verbose_name='Filtrelenmiş kullanıcı listesi')
    animate_status = models.BooleanField(default=True,verbose_name='Animasyon Durum')
    status = models.BooleanField(default=True,verbose_name='Durum')
    
    def __str__(self) -> str:
        return str(self.raffle_id)
        
# class Raffle_User_Member(models.Model):
#     id = models.BigIntegerField(primary_key=True, auto_created=True,serialize= False, verbose_name='ID')
#     raffle_id = models.ForeignKey(Raffle,on_delete=models.CASCADE, verbose_name='Çekiliş Numarası')
#     user_id = models.ForeignKey(User,on_delete=models.CASCADE, verbose_name='')
#     member_id = models.ForeignKey(Members_Classes,on_delete=models.CASCADE, verbose_name='')
#     date = models.DateTimeField(auto_now_add=True, blank=True)
#     status =models.BooleanField(default=True,verbose_name='Durum')