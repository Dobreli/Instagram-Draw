# Generated by Django 3.2.6 on 2021-10-23 21:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('members', '0004_alter_member_offers_price'),
        ('bank', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(verbose_name='Ödeme')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('status', models.BooleanField(default='True', verbose_name='Ödeme Durumu')),
                ('offer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='members.member_offers', verbose_name='Ürün Teklif No')),
            ],
            options={
                'verbose_name': 'Ödemeler',
                'verbose_name_plural': 'Ödemeler',
            },
        ),
        migrations.CreateModel(
            name='Payment_Type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_name', models.CharField(max_length=50, verbose_name='Ödeme Tipi')),
                ('status', models.BooleanField(default='True', verbose_name='Banka Durumu')),
            ],
            options={
                'verbose_name': 'Ödeme Tipi',
                'verbose_name_plural': 'Ödeme Tipi',
            },
        ),
        migrations.CreateModel(
            name='Payment_transfer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference_no', models.IntegerField(verbose_name='Referans numarası')),
                ('status', models.BooleanField(default='False', verbose_name='Havale Durumu')),
                ('bank_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bank.bank', verbose_name='Banka no')),
                ('payment_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bank.payment', verbose_name='Ödeme No')),
            ],
            options={
                'verbose_name': 'Havale/Eft',
                'verbose_name_plural': 'Havale/Eft',
            },
        ),
        migrations.AddField(
            model_name='payment',
            name='payment_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bank.payment_type', verbose_name='Ödeme Tipi'),
        ),
        migrations.AddField(
            model_name='payment',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Kullanıcı No'),
        ),
    ]
