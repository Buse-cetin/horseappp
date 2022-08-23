import requests
from smtplib import SMTP
from horseapp.movies.models import Message




def MailSender(target,message):
 try:
                # Mail Mesaj Bilgisi 
                subcjet = target.get('subject')
                message = target.get('text')
                content = "Subject: {0}\n\n{1}".format(subcjet,message)

                # Hesap Bilgileri 
                myMailAdress = "buseetinn@gmail.com"
                password = "zwgmhpyrfbtqnhlr"

                # Kime Gönderilecek Bilgisi
                sendTo = target.get('User')

                #host, port
                mail = SMTP("smtp.gmail.com", 587)
                #sunucuya bağlanma
                mail.ehlo()
                #verileri şifreleme
                mail.starttls()
                #mail sunucusunda oturum açma
                mail.login(myMailAdress,password)
                #maili gönderme
                mail.sendmail(myMailAdress, sendTo, content.encode("utf-8"))
                print("Mail Gönderme İşlemi Başarılı!")
 except Exception as e:
                print("Hata Oluştu!\n {0}".format(e)) 
                
