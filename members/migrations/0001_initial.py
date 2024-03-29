# Generated by Django 3.2.6 on 2021-09-28 23:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='members_classes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Üyelik Adı')),
                ('content', models.TextField(max_length=300, verbose_name='Açıklama')),
                ('coment_limit', models.IntegerField(max_length=10, verbose_name='Çekilecek Yorum Limiti')),
                ('tag_permission', models.BooleanField(default=False, verbose_name='Etiket İzni')),
                ('follow_permission', models.BooleanField(default=False, verbose_name='Takip İzni')),
                ('text_permission', models.BooleanField(default=False, verbose_name='Yazı Kontrol İzni')),
                ('status', models.BooleanField(default=True, verbose_name='Durum')),
            ],
            options={
                'verbose_name': 'Üyelik Sınıfları',
                'verbose_name_plural': 'Üyelik Sınıfları',
            },
        ),
        migrations.CreateModel(
            name='user_member_class',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('n_times', models.IntegerField(max_length=10, verbose_name='Kalan Hakkı')),
                ('status', models.BooleanField(default='False', verbose_name='Sınıf Durumu')),
                ('member_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='members.members_classes', verbose_name='Üyelik Sınıf Id')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User Id')),
            ],
            options={
                'verbose_name': 'Kullanıcı Üye Sınıf Bilgileri',
                'verbose_name_plural': 'Kullanıcı Üye Sınıf Bilgiler',
            },
        ),
        migrations.CreateModel(
            name='member_offers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('n_times', models.IntegerField(max_length=10, verbose_name='Adet')),
                ('price', models.IntegerField(max_length=10, verbose_name='Fiyat')),
                ('status', models.BooleanField(default=True, verbose_name='Durum')),
                ('member_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='members.members_classes', verbose_name='Member Id')),
            ],
            options={
                'verbose_name': 'Üyelik Sınıf Teklifleri',
                'verbose_name_plural': 'Üyelik Sınıf Teklifleri',
            },
        ),
    ]
