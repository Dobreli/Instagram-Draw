# Generated by Django 3.2.6 on 2021-10-25 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0006_alter_payment_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment_transfer',
            name='reference_no',
            field=models.CharField(max_length=100, verbose_name='Referans numarası'),
        ),
    ]
