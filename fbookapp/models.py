from django.db import models
import re
import bcrypt
from django.utils.datastructures import MultiValueDictKeyError

class logandregManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['firstname']) < 2:
            errors["firstname"] = "please fill the  firstname field at least 2 char"

        if len(postData['lastname']) < 2:
            errors["lastname"] = "please fill the lastname field at least 2 char"
        
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):    # test whether a field matches the pattern            
            errors['email'] = "Invalid email address!"
       
        if postData['takenemailname'] == "taken":
            errors['email2'] = "email is taken"

        if len(postData['pass']) < 8:
            errors["pass"] = "please type at least 8 char in rhe password  fiald"

        if postData['pass'] != postData['passconf']:
            errors["pass1"] = "please type the confirmed password correctly"
        return errors
    

    def book_validator(self, postData):
        errors = {}
        if len(postData['title']) < 1 or  len(postData['desc'])  < 1:
             errors["both"] = "empty field"
        else:
            if len(postData['desc']) < 5:
                errors["desc"] = "please fill the description field at least 2 char"
        return errors


    def login_validator(self, postData):

        errors = {}
        if len(postData['email']) < 1:
            errors["logemail"] = "empty email field"

        user = User.objects.filter(email=postData['email']) # why are we using filter here instead of get?
        if user: # note that we take advantage of truthiness here: an empty list will return false
            # if not bcrypt.checkpw(postData['pass'].encode(), logged_user.password.encode()):
            if not bcrypt.checkpw( postData["pass"].encode(), User.objects.get(email=postData['email']).password.encode()):
                errors["logpass"] = "the password is wrong"
        else:
            errors["logemail2"] = "not registred"
            
        return errors

class User (models.Model):
    firstname = models.CharField(max_length=45)
    lastname = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length = 45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = logandregManager()

class book (models.Model):
    title = models.CharField(max_length=45)
    desc = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uploaded_by = models.ForeignKey(User, related_name= "user", on_delete = models.CASCADE)
    User_who_like = models.ManyToManyField(User, related_name="Liked_book")
    objects = logandregManager()

    @property
    def getallusers(self):
        return self.User_who_like.all()

   
 
       

    # def __repr__(self):
    #     return f"<item = {self.item}> , id: {self.id}, wisher{self.wisher}, likes{self.likes}, created_at{self.created_at},granted_at{self.granted_at} " 

   