# Generated by Django 3.2.7 on 2022-08-20 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0013_auto_20220820_1925'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='information',
            name='image',
        ),
        migrations.AddField(
            model_name='information',
            name='imageUrl',
            field=models.CharField(max_length=50, null=True, verbose_name='Resim Url'),
        ),
        migrations.AddField(
            model_name='user',
            name='imageUrl',
            field=models.CharField(max_length=50, null=True, verbose_name='Resim Url'),
        ),
    ]
