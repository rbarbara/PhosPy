from django.db import models

# Create your models here.

# Basismodell 
class BasisModell(models.Model):
    touched = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add = True)

    class Meta:
        abstract = True


# Kläranlage
class Kläranlage(BasisModell):
    name = models.CharField(max_length = 50, unique = True)
    wert_1 = models.FloatField()
