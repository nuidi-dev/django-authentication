# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import uuid
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext as _

class AccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        user = self.model(
            email=email,
            username=username
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(email, username, password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user

class Account(PermissionsMixin, AbstractBaseUser):
    email = models.EmailField(unique=True, verbose_name=_('E-mail'), error_messages={'unique':_("This email has already been registered.")})
    username = models.CharField(unique=True, max_length=30, verbose_name=_('Username'), error_messages={'unique':_("This username has already been registered.")})
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    key = models.UUIDField(default=uuid.uuid4)
    keytime = models.DateTimeField(null=True)

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.username

    def set_new_key(self):
        self.key = uuid.uuid()
        self.save()
        return self.key

    def __unicode__(self):
        return self.username
