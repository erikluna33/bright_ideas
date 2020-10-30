from django.db import models
import re
import bcrypt
email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def basic_validator(self, post_data):
        errors = {}

        if len(post_data['first_name']) < 2:
            errors['first_name'] = " First name must be at least 2 characters"
        if len(post_data['last_name']) < 2:
            errors['last_name'] = "Last name must be at least 2 characters"
        if not email_regex.match(post_data['email']):
            errors['email'] = ("Invalid email address!")
        existing_user = User.objects.filter(email=post_data['email'])
        if len(existing_user) > 0:
            errors['email'] = "Email already in use"
        if len(post_data['password']) < 8:
            errors['password'] = "Password must be at least 8 characters"
        if len(post_data['password']) == 0:
            errors['password'] = "Password is required"
        elif len(post_data['password']) < 8:
            errors['password'] = "Password must be at least 8 characters long"
        elif post_data['password'] != post_data['confirm_pw']:
            errors['password'] = "Password and Confirm Password inputs must match"
        return errors
    

    def log_validator(self, post_data):
        errors = {}
        if len(post_data['email']) == 0:
            errors['email'] = "Email is required"
        elif not email_regex.match(post_data['email']):
            errors['email'] = ("Invalid email address!")
        existing_user = User.objects.filter(email=post_data['email'])
        if len(existing_user) != 1:
            errors['email'] = "User not found"
        if len(post_data['password']) == 0:
            errors['password'] = "Password is required"
        elif len(post_data['password']) < 8:
            errors['password'] = "Password must be at least 8 characters"
        elif bcrypt.checkpw(post_data['password'].encode(), existing_user[0].password.encode()) != True:
            errors['email'] = "Email and password do not match"
        
        return errors
    
    def add_validator(self, post_data):
        errors = {}
        if len(post_data['first_name']) < 2:
            errors['first_name'] = " First name must be at least 2 characters"
        if len(post_data['last_name']) < 2:
            errors['last_name'] = "Last name must be at least 2 characters"
        if not email_regex.match(post_data['email']):
            errors['email'] = ("Invalid email address!")
        existing_user = User.objects.filter(email=post_data['email'])
        if len(existing_user) > 0:
            errors['email'] = "Email already in use"
        if len(post_data['password']) < 8:
            errors['password'] = "Password must be at least 8 characters"
        if len(post_data['password']) == 0:
            errors['password'] = "Password is required"
        elif len(post_data['password']) < 8:
            errors['password'] = "Password must be at least 8 characters long"
        elif post_data['password'] != post_data['confirm_pw']:
            errors['password'] = "Password and Confirm Password inputs must match"
        return errors

    def update_validator(self, post_data):
        errors = {}
        if len(post_data['first_name']) < 2:
            errors['first_name'] = " First name must be at least 2 characters"
        if len(post_data['last_name']) < 2:
            errors['last_name'] = "Last name must be at least 2 characters"
        if not email_regex.match(post_data['email']):
            errors['email'] = ("Invalid email address!")
        existing_user = User.objects.filter(email=post_data['email'])
        if len(existing_user) > 0:
            errors['email'] = "Email already in use"
        return errors
    
    def idea_validator(self, post_data):
        errors = {}
        if len(post_data['idea']) < 1:
            errors['idea'] = "Please fill in your idea"
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=60)
    user_level = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Idea(models.Model):
    idea = models.TextField()
    user = models.ForeignKey(User, related_name='ideas', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    comment = models.CharField(max_length=255)
    poster = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    wall_idea = models.ForeignKey(Idea, related_name='post_comments', on_delete=models.CASCADE)