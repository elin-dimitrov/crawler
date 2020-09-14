from django.db import models
# Create your models here.


class Politic(models.Model):
      minister_name = models.CharField(max_length=255, blank=False, null=True, unique=False)
      email = models.EmailField(null=True, blank=False)
      party = models.CharField(max_length=64, blank=False, null=True)
      date_of_birth = models.CharField(max_length=10, blank=False, null=True)
      place_of_birth = models.CharField(max_length=64, blank=False, null=True)
      languages = models.CharField(max_length=64, blank =False, null=True)
      proffesion = models.CharField(max_length=128, blank=False, null=False)
      
      
      def __str__(self):
         return self.minister_name