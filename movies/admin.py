from django.contrib import admin
from .models import  Ip, Product, Smmtp, User, Information, Message


    
# Register your models here.
admin.site.register(Product),
admin.site.register(User),
admin.site.register(Information),
admin.site.register(Message),
admin.site.register(Ip),
admin.site.register(Smmtp)