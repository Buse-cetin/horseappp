from tabnanny import verbose
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.CharField(max_length=200)
    imageUrl = models.CharField(max_length=50)

    

class User(models.Model):
    name = models.CharField("Ad",max_length=200)
    surname = models.CharField("Soyad",max_length=200)
    email = models.EmailField()
    imageUrl = models.CharField("Resim Url",max_length=50, null=True)

    def __str__(self):
        return f"{self.name} {self.surname}"
    

class Message(models.Model):
    subject = models.CharField("Konu",max_length=200)
    text = models.CharField("İçerik",max_length=200)
    User = models.ForeignKey("Kime",User, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField("Tarih",auto_now=True)

    def __str__(self):
       return self.subject 

class Information(models.Model):
    title = models.CharField("Başlık",max_length=200)
    subtitle = models.CharField("Alt Başlık",max_length=200)
    informate = models.CharField("Bilgi",max_length=200)
    imageUrl = models.CharField("Resim Url",max_length=50, null=True)

    class Meta:
        verbose_name = "Bilgi"
        verbose_name_plural = "Bilgiler"

    def __str__(self):
       return self.title
    

class Smmtp(models.Model):
    port = models.DecimalField(max_digits=8, decimal_places=2)
    host = models.EmailField()
    smtpsecure = models.CharField(max_length=200)

class Other(models.Model):
    see = models.CharField(max_length=200)

   # genders = (
    #    ('E','Erkek')
     #   ('K','Kadın')
    #)

    #gender = models.CharField(max_length=1, choices=genders)



    #date = models.DateTimeField(auto_now=True) #mesaj gönderdiğimde otomatik olarak o anki tarih bilgisini ve sattini ekleyecek.
  
