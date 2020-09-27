import smtplib
from email.message import EmailMessage, MIMEPart

from django.http import HttpResponse
from django.shortcuts import render

from mails.models import Email
from mails.forms import EmailForm

from mails.custom import parse_images_to_base64
# Create your views here.

def home(request):
    return HttpResponse("You're at Mails Home") 



def new(request):
    if request.method == "GET":
        # test data
        data = {'subject': "hello",
                "sender": "sender@mail.com",
                "receiver": "receiver@mail.com"}
        form = EmailForm(data)
        return render(request, 'mails/new.html', context={'form':form})

    elif request.method == "POST":
        data = request.POST
        from_email = data['sender']
        to_email = data['receiver']
        subject = data['subject']
        content = data['content']
        print(content)
        content_html_image_encoded = parse_images_to_base64(content)

        msg = EmailMessage() 
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject
        
        msg.make_mixed()

        html_part = MIMEPart()
        html_part.set_content(content_html_image_encoded, subtype="html")
        
        msg.attach(html_part)

        with smtplib.SMTP("smtp.mailtrap.io", 2525) as server:
            server.login("2391789313484d", "96d048bb6390e0")
            server.send_message(msg)

        return HttpResponse("Message Sent Successfully: "+content)
