from django.db import models
import datetime
import re, bcrypt

class UserManager(models.Manager):
    def validate_register(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name should be at least 2 characters."
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name should be at least 2 characters."
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address."
        if User.objects.filter(email=postData['email']):
            errors['email'] = "Email already exist."
        if len(postData['password']) < 8:
            errors['password'] = "Password should be at least 8 characters."
        if postData['password'] != postData['confirm_pw']:
            errors['confirm_pw'] = "Confirm password does not match."
        if len(postData['dob']) < 1:
            errors['dob'] = "Invalid date of birth."
        elif postData['dob'] > str(datetime.date.today()):
            errors['dob'] = "Date of birth should be in past."
        else:
            if (datetime.date.today().year)-(int(postData['dob'][0:4])) < 13:
                errors['dob'] = "You are under 13."
        return errors
    
    def validate_login(self, postData):
        errors = {}
        user = User.objects.filter(email=postData['email'])
        if len(postData['email']) < 1:
            errors['email'] = "Email should be at least 8 characters."
        elif not user:
            errors['email'] = "Username is not found."
        else:
            if not bcrypt.checkpw(postData['password'].encode(), user[0].password.encode()):
                errors['password'] = "Incorrect password!"
        if len(postData['password']) < 8:
            errors['password'] = "Password should be at least 8 characters."
        return errors

    def validate_success(self, postData):
        errors={}
        if 'user_name' not in postData:
            errors['permission'] = "Permission Denied."
        return errors

class User(models.Model):
    first_name = models.CharField(max_length = 45)
    last_name = models.CharField(max_length = 45)
    email = models.CharField(max_length = 45)
    password = models.CharField(max_length = 255)
    dob = models.DateField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()