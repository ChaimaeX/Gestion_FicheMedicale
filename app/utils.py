from django.shortcuts import get_object_or_404
from .models import *
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

def incrementer_numero(annee):
    num = FicheNum.objects.filter(annee=annee).first()
    if num :
       num.num_f +=1
       num.save()
       return num.num_f
    else:
        obj = {
            "annee": annee,
            "num_f":1,

        }  
        created = FicheNum.objects.create(**obj)
        return 1

def get_context_data(self, pk):
        
        try:
            

            client = get_object_or_404(Maladie, pk=pk)
            fiches_medicales = client.fiches_medicales.all()
            first_fiche = fiches_medicales.order_by('date').first()
            annee_actuelle = first_fiche.date.strftime("%y") if first_fiche else ""
            context = {
                'list':fiches_medicales,
                'client':client,
                'annee_actuelle':annee_actuelle,
            }
        except ObjectDoesNotExist as e:
            messages.error(self.request, f"Erreur de récupération des données : {e}")
            context = {}
        return context