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

    def test_redirect_if_not_logged_in(self):
        """
        if user is not logged in then reverse('new') will redirect to reverse('login').
        reverse('profile') will redirect to reverse('login')
        """
        c = Client()
        resp = c.get(reverse('new'))
        self.assertRedirects(resp, '/mails/accounts/login/?next=/mails/new/')

        resp = c.get(reverse('profile'))
        self.assertRedirects(resp, '/mails/accounts/login/?next=/mails/accounts/profile/')
   
   """
   test BulkEmail save() only after sending emails
   """
