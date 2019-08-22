from django.db import models
from datetime import date, datetime
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# thing ='2015-01-01'
# t3 = date.today() - datetime.strptime(thing + ' ' + '12:00:00', '%Y-%m-%d %H:%M:%S').date()
# print(t3)
# yeardiff = t3.total_seconds() / 31536000
# if yeardiff < 13:
#     print('yay!')
# print(yeardiff)

class UserManager(models.Manager):
    def basic_validator(self, postData):
        # print('START OF VALIDATOR')
        # print('*'*100)
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first-name'] = "First name must contain at least 2 characters"
        if len(postData['last_name']) < 2:
            errors['last-name'] = "Last name must contain at least 2 characters"
        if len(postData['birthday']) < 1:
            errors['birthday'] = "Must enter a valid birthday"
        else:
            if datetime.strptime(postData['birthday'] + ' ' + '12:00:00', '%Y-%m-%d %H:%M:%S').date() > date.today():
                errors['birthday'] = "Cannot enter a future date for a birthday"
            if datetime.strptime(postData['birthday'] + ' ' + '12:00:00', '%Y-%m-%d %H:%M:%S').date() < date.today():
                findtime = date.today() - datetime.strptime(postData['birthday'] + ' ' + '12:00:00', '%Y-%m-%d %H:%M:%S').date()
                yeardiff = findtime.total_seconds() / 31536000
                if yeardiff < 13:
                    errors['birthday'] = "Must be at least 13 years of age to register"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Must be a valid email address"
        if len(postData['password']) < 8:
            errors['password'] = "Password must contain at least 8 characters"
        if postData['password'] != postData['confirmpassword']:
            errors['password'] = "Passwords must match"
        try:
            # print(postData['email'])
            findme = User.objects.get(email=postData['email'])
            # print('IN EMAIL TRY')
            # print(findme)
            # print('*'*100)
        except User.DoesNotExist:
            # print('IN EMAIL EXCEPT')
            # print('*'*100)
            findme = None
        if findme:
            # print('IN EMAIL FOUND')
            # print('*'*100)
            errors['email'] = "That email is already registered"
        # print('END VALIDATOR')
        # print('*'*100)
        return errors
    
    def login_validator(request, postData):
        errors = {}
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Must be a valid email address"
        try:
            findme = User.objects.get(email=postData['email'])
        except User.DoesNotExist:
            findme = None
            errors['email'] = "That email is not yet registered"
        if findme:
            print('yay')
            # print(findme.password)
        if bcrypt.checkpw(postData['password'].encode(), findme.password.encode()):
            print('password match')
        else:
            errors['password'] = "Wrong password entered"

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birthday = models.CharField(max_length=25)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
