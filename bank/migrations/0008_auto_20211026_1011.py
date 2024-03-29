# Generated by Django 3.2.6 on 2021-10-26 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0007_alter_payment_transfer_reference_no'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='check_status',
            field=models.BooleanField(default='True', verbose_name='Sipariş Durumu'),
        ),
        migrations.AddField(
            model_name='payment_transfer',
            name='check_status',
            field=models.BooleanField(default='False', verbose_name='Havale İncelenme Durumu'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='status',
            field=models.BooleanField(default='False', verbose_name='Ödeme Durumu'),
        ),
    ]
