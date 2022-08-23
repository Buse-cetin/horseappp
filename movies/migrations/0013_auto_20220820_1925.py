# Generated by Django 3.2.7 on 2022-08-20 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0012_auto_20220819_1309'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='Users',
            new_name='users',
        ),
        migrations.RemoveField(
            model_name='information',
            name='imageUrl',
        ),
        migrations.RemoveField(
            model_name='user',
            name='imageUrl',
        ),
        migrations.AddField(
            model_name='information',
            name='image',
            field=models.ImageField(blank=True, upload_to='images/', verbose_name='Resim Url'),
        ),
        migrations.AddField(
            model_name='user',
            name='image',
            field=models.ImageField(blank=True, upload_to='images/', verbose_name='Resim Url'),
        ),
    ]