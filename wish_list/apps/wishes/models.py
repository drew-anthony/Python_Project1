from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9+_-]+@[a-zA-z0-9+_-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def validate(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First Name must be longer than 2 charaters"
        if len(postData['first_name']) > 255:
            errors["first_name"] = "First Name must be shorter than 255 charaters"
        if len(postData['last_name']) < 2:
            errors["last_name"] = 'Last Name must be longer than 2 characters'
        if len(postData['last_name']) > 255:
            errors["last_name"] = 'Last Name must be shorter than 255 characters'
        if len(postData['email']) < 8:
            errors["email"] = 'Email must be at least 8 characters long'
        if len(postData['email']) > 255:
            errors["email"] = 'Email must be at shorter than 8 characters long'
        elif not EMAIL_REGEX.match(postData['email']):
            errors['email'] = 'Email not in email format'
        if len(postData['password']) < 8:
            errors["password"] = "Password must be 8 characters long"
        if len(postData['password']) > 255:
            errors["password"] = "Password must be shorter than 8 characters long"
        if postData['confirm_password'] != postData['password']:
            errors['confirm_password'] = "Passwords do not match"
        return errors
        
    def create_user(self, postData):
        hash_pass = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
        user = self.create(
            first_name = postData['first_name'],
            last_name = postData['last_name'],
            email = postData['email'],
            password = hash_pass,
        )
        return user

    def validateLogin(self, postData):
        errors = {}
        if len(postData['email']) < 1:
            errors['username'] = 'Email must be populated'
        if User.objects.filter(email=postData['email']).exists():
            user = User.objects.get(email=postData['email'])
            if not bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
                errors['password'] = 'E-mail password combination is incorrect.'
        else:
            errors['mail'] = 'E-mail password combination is incorrect.'
        return errors

class ItemManager(models.Manager):
    def validateItem(self,postData):
        errors = {}
        if len(postData['item/product']) < 1:
            errors["item/product"] = "Item field must be populated"
        if len(postData['item/product']) > 255:
            errors["item/product"] = "Item field must be less than 255 characters"
        return errors

    def create_item(self, postData):
        item = self.create(
            name = postData ['item/product'],
            created_by = postData['created_by'],
        )
        return item


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

class Item(models.Model):
    name = models.CharField(max_length=255)
    created_by = models.CharField(max_length=255)
    item_owner = models.ManyToManyField(User, related_name="owned_item")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)   

    objects = ItemManager()

    def __str__(self):
        return "{} - {}".format(self.id, self.email)