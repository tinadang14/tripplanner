
from __future__ import unicode_literals

from django.db import models
import datetime
import re, md5
import binascii
from os import urandom
from datetime import datetime


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PW_REGEX = re.compile(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$')

# Create your models here.
class UserManager(models.Manager):
    def addUser(self, person):
        response = {}
        errors = []
        if len(person["first_name"])<2 or len(person["last_name"]) < 2:
            errors.append("your first & last name needs to be more than 2 characters")
        if len(person["email"]) < 1:
            errors.append("Email cannot be blank!")
        if not EMAIL_REGEX.match(person["email"]):
            errors.append("This email is invalid")
        if User.objects.filter(email = person["email"]):
            errors.append("email's taken!")
        if len(person["pw"]) < 7:
            errors.append("password must be at least 8 characters")
        if not PW_REGEX.match(person["pw"]):
            errors.append("Password should be min. 8 characters, 1 alphabet, & 1 number")
        if not (person["pw"]) == (person["confpw"]):
            errors.append("passwords must match!")
        if errors:
            response['status'] = False
            response['errors'] = errors
        else:
            salt = binascii.b2a_hex(urandom(15))
            hashed_pw = md5.new(person["pw"]+salt).hexdigest()
            response['status'] = True
            response['person'] = User.objects.create(first_name=person["first_name"], last_name=person["last_name"], email=person["email"], pw=hashed_pw, salt=salt)
        return response

    def ValUser(self, person):
        response = {}

        try:
            print "VALUSER = TRYING"
            user= User.objects.get(email = person["email"])
            hashed_pw = md5.new(person["pw"]+user.salt).hexdigest()

            if user.pw == hashed_pw:
                print ""
                response ["status"]= True
                response ["user"]= user
                return response
            else:
                print "we dont wanna be here"
                response ["status"] = False
                return response
        except:
            print "we are in except"
            response ["status"] = False
            return response

class User(models.Model):
    first_name = models.CharField(max_length=16)
    last_name = models.CharField(max_length=16)
    email = models.CharField(max_length=40)
    pw = models.CharField(max_length=16)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    salt = models.TextField()

    objects = UserManager()
