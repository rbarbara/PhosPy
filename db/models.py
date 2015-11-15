from django.db import models

# Create your models here.
# Basismodell
class BasisModell(models.Model):
    created = models.DateTimeField(auto_now_add = True)
    touched = models.DateTimeField(auto_now = True)

    class Meta:
        abstract = True

class Klaeranlage(BasisModell):
    name = models.CharField()