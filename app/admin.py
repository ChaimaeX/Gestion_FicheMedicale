from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import *
# Register your models here.

class Adminclient(admin.ModelAdmin):
    list_display = ('nom' ,'num_fiche','adresse','tel')

class AdminFiche(admin.ModelAdmin):
    list_display= ('maladie','date','dent','honoraires')

   
class adminNombreFacture(admin.ModelAdmin):
    list_display= ('annee','num_f')


admin.site.register(Maladie,Adminclient)
admin.site.register(FicheMedicale,AdminFiche)
admin.site.register(FicheNum)
