# What?
A simple-painless bulk emailer you can use in your localhost to create and design the emails (using Froala Editor), and send with your `outlook` account. Also there's an outbox for previously sent emails.
# Install
```
git clone https://github.com/riyadhrazzaq/bulky.git
cd bulky
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

# HowTo
## Send Email
1. go to `127.0.0.1:8000/mails/signup/` to create a new account.
2. log in from `127.0.0.1:8000/mails/signup/`.

# Stack
1. Django
2. Django Templates
3. Python's `email` module
4. Bulma (css framework)
5. Froala Editor for WYSIWYG editor
