import sys
import smtplib
import mimetypes
from email.message import EmailMessage, MIMEPart

from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
from django.contrib import messages

from mails.forms import EmailForm
from mails.models import BulkEmail
from mails.custom import parse_images_to_base64, send_mail_with_outlook

# from mails.custom import get_attachments_from_uploads
# Create your views here.


def home(request):
    return HttpResponse("Desing Landing Page")

@login_required
def new(request):
    if request.method == "GET":
        # test data
        data = {
            "subject": "testing from outlook",
            "sender": "riyadhrazzaq@outlook.com",
        }
        form = EmailForm(data)
        return render(request, "mails/new.html", context={"form": form})

    elif request.method == "POST":
        # getting textual data from FORM
        data = request.POST
        # getting files data from FORM
        files = request.FILES.getlist("attachments")

        from_email = data["sender"]
        receipients = [e.strip() for e in data["receiver"].split("\n")]
        subject = data["subject"]
        content = data["content"]
        content_html_image_encoded = parse_images_to_base64(content)

        # creating msg object part by part
        msg = EmailMessage()
        msg["From"] = from_email
        msg["Subject"] = subject

        msg.make_mixed()

        # content
        html_part = MIMEPart()
        html_part.set_content(content_html_image_encoded, subtype="html")

        msg.attach(html_part)

        # attachment
        if len(files) > 0:
            for f in files:
                maintype, subtype = f.content_type.split("/")
                msg.add_attachment(
                    f.read(),
                    maintype=maintype,
                    subtype=subtype,
                    filename=f.name,
                    disposition="attachment",
                )

        # with smtplib.SMTP("smtp.mailtrap.io", 2525) as server:
        # server.login("2391789313484d", "96d048bb6390e0")
        # for to in to_email:
        # msg['To'] = to
        # server.send_message(msg)
        # del msg['To']

        with smtplib.SMTP("smtp.office365.com", 587) as server:
            server.ehlo()
            server.starttls()
            server.login(data['outlook_email'], data['outlook_password'])
            for to in receipients:
                msg['To'] = to
                server.send_message(msg)
                del msg['To']

        # creating bulkmail and save to db
        data = {
            "author": request.user,
            "sender": from_email,
            "receiver": receipients,
            "subject": subject,
            "content": content,
            "date": timezone.now(),
        }
        this_bulk = BulkEmail(**data)
        this_bulk.save()
        messages.add_message(request, messages.SUCCESS, "Mail Sent!")
        return redirect("profile")


def signup_view(request):
    if request.user.is_authenticated:
        return redirect("profile")
    else:
        if request.method == "GET":
            form = UserCreationForm()
            return render(request, "registration/signup.html", context={"form": form})

        elif request.method == "POST":
            form_data = request.POST
            form = UserCreationForm(form_data)
            if form.is_valid():
                form.save()
                return redirect("login")
            else:
                errors = form.errors
                print(errors)
                return render(request, "registration/signup.html", context={"form": form, "errors": errors})

@login_required
def profile_view(request):
    bulks_by_user = BulkEmail.objects.filter(author=request.user)
    return render(
        request, "registration/profile.html", context={"bulks_by_user": bulks_by_user}
    )


@login_required
def message_detail(request, pk):
    query_set = BulkEmail.objects.filter(author=request.user)
    obj = get_object_or_404(query_set, pk=pk)
    return render(request, "mails/detail.html", context={"bulkmail_obj": obj})
