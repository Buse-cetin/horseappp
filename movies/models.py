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
   # image = models.ImageField("Resim Url",blank=True, upload_to='images/',null=True)
    def __str__(self):
        return f"{self.name} {self.surname}"

    class Meta:
        verbose_name = "Kişi"
        verbose_name_plural = "Kişiler"
        


class Message(models.Model):
    subject = models.CharField("Konu",max_length=200)
    text = models.CharField("İçerik",max_length=2500)
    Users = models.ManyToManyField(User)
   # User = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    #User = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField("Tarih",auto_now=True, null=True)

    def __str__(self):
       return self.subject 

    class Meta:
        verbose_name = "Mesaj"
        verbose_name_plural = "Mesajlar"
       

class Information(models.Model):
    title = models.CharField("Başlık",max_length=200)
    subtitle = models.CharField("Alt Başlık",max_length=200, null=True)
    informate = models.CharField("Bilgi",max_length=5000)
    imageUrl = models.ImageField("Resim Url",blank=True,null=True)

    class Meta:
        verbose_name = "Bilgi"
        verbose_name_plural = "Bilgiler"

    def __str__(self):
       return self.title

class Smmtp(models.Model):
    port = models.DecimalField(max_digits=8, decimal_places=0)
    host = models.CharField(max_length=200)
    smtpsecure = models.CharField(max_length=200)

    class Meta:
        verbose_name = "SMTP"
        verbose_name_plural = "SMTP Ayarları"

class Ip(models.Model):
    ip = models.GenericIPAddressField(null=True)
   # ipp = models.CharField(max_length=200)

    class Meta:
        verbose_name = "İp Adres"
        verbose_name_plural = "İp Adresler"

class Other(models.Model):
    see = models.CharField(max_length=200)

class Example(models.Model):
    see = models.CharField(max_length=200)



