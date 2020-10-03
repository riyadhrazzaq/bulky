from django.shortcuts import reverse
from django.test import TestCase, Client
from django.contrib.auth.models import User
from mails.models import BulkEmail

# Create your tests here.

class MailsViewTest(TestCase):
    def setUp(self):
        # create two user
        test_user_1 = User.objects.create(username='testuser1', password='testpass1')
        test_user_2 = User.objects.create(username='testuser2', password='testpass2')

        test_user_1.save()
        test_user_2.save()

        self.test_form_bulkemail = {'sender': 'testuser1@mail.com',
                'receiver': 'testuser2@mail.com',
                'subject': 'hello world',
                'content': 'this is message',
                'attachments': '',
                'outlook_email': 'test_ol@mail.com',
                'outlook_password': 'blah'}

        # valid login html
        c = Client()
        resp = c.get(reverse('login'))
        self.valid_login_html = resp.content.decode('utf-8')

    def test_redirect_if_not_logged_in(self):
        """
        if user is not logged in then reverse('new') will redirect to reverse('login').
        reverse('profile') will redirect to reverse('login')
        """
        c = Client()
        resp = c.get(reverse('new'))
        self.assertRedirects(resp, '/mails/login/?next=/mails/compose/')

        resp = c.get(reverse('profile'))
        self.assertRedirects(resp, '/mails/login/?next=/mails/profile/')
        # post url 'new'
        resp = c.post(reverse('new'), self.test_form_bulkemail)
        self.assertEqual(resp.status_code, 302)

    def test_access_logged_in(self):
        """
        if user is logged in reverse('new') will return status code 200,
        reverse('profile') will return status code 200, reverse('login','signup') will return "You're already logged in" message.
        """
        c = Client()
        c.login(username='testuser1', password='testpass1')
        
        # url 'login'
        resp = c.get(reverse('login'), follow=True)
        self.assertTemplateNotUsed(template_name='registration/login.html')

        # url 'signup'
        resp = c.get(reverse('signup'), follow=True)
        self.assertTemplateNotUsed('registration/signup.html')
