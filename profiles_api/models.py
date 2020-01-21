from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.conf import settings
from django.core.validators import MinLengthValidator


import datetime


class UserProfileManager(BaseUserManager):
    '''Manager for user profiles'''

    def create_user(self, email, name, password=None):
        '''Create a new user profile'''
        if not email:
            raise ValueError("User must have an email")

        email = self.normalize_email(email)
        user = self.model(email=email, name=name)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):
        '''Create a super user'''
        user = self.create_user(email, name, password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    '''Database models for users in the system'''
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name',]

    def get_full_name(self):
        '''Retrieve full name of user'''
        return self.name

    def get_short_name(self):
        '''Retrieve short name of user'''
        return self.name

    def __str__(self):
        '''Retrieve string representation of the user'''
        return self.email


class ProfileFeedItem(models.Model):
    user_profile = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    status_text = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.status_text


class College(models.Model):
    '''Database model for Colleges'''
    name = models.CharField(max_length = 150)
    location = models.CharField(max_length = 150)

    def __str__(self):
        '''Retrieve string representation of the College'''
        return self.name + ", " + self.location


class Issue(models.Model):
    '''Database model for Issue category'''
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class UserDetails(models.Model):
    '''User profile details'''
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    college = models.ForeignKey(
        College,
        on_delete=models.CASCADE,
    )
    roll_no = models.IntegerField()
    #dp = models.ImageField(null=True)
    department = models.CharField(max_length=100)
    contact = models.CharField(max_length=10, validators=[MinLengthValidator(10)])

    year = models.IntegerField(
        choices=[(r,r) for r in range(1984, datetime.date.today().year+1)]
    )


class Grievance(models.Model):
    '''Database model for Grievance reports'''
    title = models.CharField(max_length=80)
    issue = models.ForeignKey(Issue, null=True, on_delete=models.SET_NULL)
    description = models.CharField(max_length=400)
    lodger = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    #created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        '''Retrieve string representation of the Grievance'''
        return self.title + self.lodger
