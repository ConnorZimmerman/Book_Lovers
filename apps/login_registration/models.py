#Login_registration Models
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.core import validators 
import re
import bcrypt
import datetime


# Create your models here.
class UserManager(models.Manager):
    def login_validator(self, postData):
        response = {
            'status' : True,
            'errors' : []
            }
        try:
            user = self.get(email = postData["email"])
        except:
            user = None
        if not user:
            response["errors"].append("Email is not registered!")
        if user:
            if not bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
                response["errors"].append("Password does not match registered email.")
        if len(response["errors"]) == 0:
            response["user"] = user
            return response
        response["status"] = False
        return response
    def registration_validator(self, postData):
        response = {
            'status' : True,
            'errors' : []
            }
        EMAIL_regex = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
        if len(postData["name"]) < 2:
            response["errors"].append("Name must be at least two characters!")
        if len(postData["alias"]) < 2:
            response["errors"].append("Alias must be at least two characters!")
        if not re.match(EMAIL_regex, postData['email']):
            response["errors"].append("Not a valid email!")
        if len(postData["password"]) < 8:
            response["errors"].append("Password must be at least 8 characters!")
        if postData["password"] != postData["confirmPassword"]:
            response["errors"].append("Passwords do not match!")
        emailObject = self.filter(email = postData["email"])
        if len(emailObject) > 0:
            response["errors"].append("Email is already in database!")
        if len(response["errors"]) == 0:
            hashed = bcrypt.hashpw((postData['password'].encode()), bcrypt.gensalt(12))
            user = self.create(name = postData["name"], alias = postData["alias"], email = postData["email"], password = hashed, review_count = 0)
            response["user"] = user
            return response
        response["status"] = False
        return response

class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    review_count = models.IntegerField()
    password = models.CharField(max_length=255)
    objects = UserManager()
    