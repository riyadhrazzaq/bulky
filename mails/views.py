import smtplib
import mimetypes
from email.message import EmailMessage, MIMEPart

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from mails.forms import EmailForm
from mails.custom import parse_images_to_base64
# from mails.custom import get_attachments_from_uploads
# Create your views here.

def home(request):
    return redirect('new')



def new(request):
    if request.method == "GET":
        # test data
        data = {'subject': "hello",
                "sender": "sender@mail.com",
                "receiver": "receiver@mail.com"}
        form = EmailForm(data)
        return render(request, 'mails/new.html', context={'form':form})

    elif request.method == "POST":
        # getting textual data from FORM
        data = request.POST
        # getting files data from FORM
        files = request.FILES.getlist('attachments')

        from_email = data['sender']
        to_email = data['receiver']
        subject = data['subject']
        content = data['content']
        content_html_image_encoded = parse_images_to_base64(content)

        # creating msg object part by part
        msg = EmailMessage() 
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject
        
        msg.make_mixed()

        # content
        html_part = MIMEPart()
        html_part.set_content(content_html_image_encoded, subtype="html")
        
        msg.attach(html_part)
        
        # attachment
        if len(files) > 0:
            for f in files:
                maintype, subtype = f.content_type.split('/')
                msg.add_attachment(f.read(), maintype=maintype, subtype=subtype,
                        filename=f.name, disposition='attachment')

        with smtplib.SMTP("smtp.mailtrap.io", 2525) as server:
            server.login("2391789313484d", "96d048bb6390e0")
            server.send_message(msg)

        return HttpResponse("Message Sent Successfully: "+content)

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == "GET":
            form = UserCreationForm()
            return render(request, 'registration/signup.html', context={'form': form})

        elif request.method == "POST":
            form_data = request.POST
            form = UserCreationForm(form_data)
            if form.is_valid():
                form.save()
                return redirect('login')
            else:
                return render(reverse('signup_view'))

@login_required
def profile_view(request, username):
    if username == request.user.username:
        return render(request, 'registration/profile.html', context={'username': username})
    return redirect('home')
