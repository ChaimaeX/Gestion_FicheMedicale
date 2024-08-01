from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

# Create your models here.
class FicheNum(models.Model):
     annee= models.IntegerField()
     num_f = models.IntegerField()
     class Meta:
          verbose_name = "Num_Fiche"
          verbose_name_plural ="Num_Fiche"
""" chaque maladie va plusieur fiche Midical """
class Maladie(models.Model):
    nom = models.CharField(max_length=132)
    num_fiche = models.IntegerField()
    adresse = models.CharField(max_length=200)
    tel = models.CharField(null=True,max_length=50)
    Observations =  models.CharField(max_length=200)
    class Meta:
          verbose_name = "Maladie"
          verbose_name_plural ="Maladies"
    def __str__(self):
          return self.nom
class FicheMedicale(models.Model):
     maladie = models.ForeignKey(Maladie, on_delete=models.CASCADE, related_name='fiches_medicales')
     date = models.DateField()
     dent = models.CharField(null=True,max_length=40)
     actes = models.CharField(max_length=132)
     honoraires = models.CharField(max_length=132)
     recu = models.CharField(max_length=132)
     reste_a_paye = models.CharField(null=True,max_length=132)

     class Meta:
          verbose_name = "FicheMedicale"
          verbose_name_plural ="FicheMedicale"
    