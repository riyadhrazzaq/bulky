"""
Helper functions.
"""
import os
import base64
import mimetypes
from urllib.parse import urlparse, unquote
from bs4 import BeautifulSoup
from django.shortcuts import redirect

def parse_images_to_base64(html):
    sp = BeautifulSoup(html, 'html.parser')
    img_tags = sp.find_all('img')
    for image in img_tags:
        # extracting file location in disk
        file_url = image['src']
        url_path = urlparse(file_url).path[1:]
        url_path = unquote(url_path)

        try:
            img_data = base64.b64encode(open(url_path, "rb").read()).decode()
        except:
            print("IN PARSING ERROR IMAGE")
            print(os.path.isfile(url_path))

        mimetype = mimetypes.guess_type(url_path)[0]
        new_src = f"data:{mimetype};base64,{img_data}"

        image['src'] = new_src
    
    return sp.prettify()


def send_mail_with_outlook(request, msg, receipients):
    if request.method == "GET":
        return render(request, 'registration/outlook.html')
    elif request.method == "POST":
        data = request.POST
        
        with smtplib.SMTP("smtp.office365.com", 587) as server:
            server.login(request.POST.username, request.POST.password)
            for to in receipients:
                msg['To'] = to
                server.send_message(msg)
                del msg['To']
        return redirect('profile')
