from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class Users(AbstractUser):
      username = models.CharField(max_length=255, blank=False, null=True, unique=True)
      email = models.EmailField(null=True, blank=False)
      last_login = models.DateTimeField(null=True, blank=True)

      def __str__(self):
         return self.username