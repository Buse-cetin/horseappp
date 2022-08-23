from django.urls import path
from . import views

urlpatterns = [
    path("", views.index), 
    path("index.html", views.index), 
    path("hakkimizda.html", views.hakkimizda ),
    path("kişimail.html", views.kişimail ),
    path("kamerakayit.html", views.kamerakayit ),
    path("kayitweb.html", views.kayitweb ),
    path("smtp.html", views.smtp ),
    path("mail.html", views.MailSender ),
    path("login.html", views.login ),
    path("404.html", views.hata ),
    path("cikis.html", views.cikis ),
    path("forgot-password.html", views.sifreu ),
    path("admin_login.html", views.admin_login ),
    path("_youtube.html", views.youtube )
]

