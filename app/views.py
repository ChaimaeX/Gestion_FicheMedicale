from django.shortcuts import get_object_or_404
import os
from django.shortcuts import render
from django.views import View
from .models import*
from django.contrib import messages
from django.db import transaction
from django.shortcuts import redirect
from .utils import incrementer_numero,get_context_data
from django.core.exceptions import ObjectDoesNotExist

class HomeView(View):
    template_name="home.html"
    
    def get(self, request, *args, **kwargs):
        # Maladie.objects.all().delete()
        clients = Maladie.objects.all()
        context={
        'clients': clients    
        }
        return render(request, self.template_name,context)
    
    def post(self, request, *args, **kwargs):
        if request.POST.get('id_supprimer'):

            try:

                maladie_id = request.POST.get('id_supprimer')
                obj = get_object_or_404(Maladie, pk=maladie_id)
                obj2 = obj.fiches_medicales.first()

                
                if obj2:
                    date_first = obj2.date.year
                   
                    print(date_first)
                    numFac = FicheNum.objects.get(annee=date_first)
                    numFac.num_f -= 1
                    numFac.save()

                obj.delete()
                messages.success(request, ("La suppression a été effectuée avec succès."))   
           
            except Exception as e:
                 messages.error(request, f"Désolé, une erreur dans cette fiche. {e}.") 

            
                    

        
        clients = Maladie.objects.all()
    
        context={
           'clients': clients    
        }
        return render(request, self.template_name,context)

class addFicheView(View):
    template_name = "addFiche.html"
    def get(self, request, *args, **kwargs):
        
        return render(request,self.template_name)
    
    @transaction.atomic()
    def post(self, request, *args, **kwargs):
      items = []
    
      client = request.POST.get('client')
      adresse = request.POST.get('adresse')
      tel = request.POST.get('tel')
      Observations = request.POST.get('Observations')
      dates = request.POST.getlist('date')
      dents = request.POST.getlist('dent')
      actes = request.POST.getlist('actes')
      honoraires = request.POST.getlist('honoraires')
      recus = request.POST.getlist('recu')
      restes = request.POST.getlist('reste')
      first_date = dates[0] 
      annee ,  mois, jour = map(int, first_date.split('-'))
      numero_facture = incrementer_numero(annee)

      if dents is None:
          dents = []
      if restes is None:
          restes = []
      if honoraires is None:
          honoraires = []

      # Création de l'objet Maladie
      client_object = {
        'nom': client,
        'num_fiche': numero_facture,
        'adresse': adresse,
        'tel': tel,
        'Observations':Observations or '',
       }
      maladie = Maladie.objects.create(**client_object)
    
      # Création des objets FicheMedicale
      for date, dent, acte, honoraire, recu, reste in zip(dates, dents, actes, honoraires, recus, restes):
        data = FicheMedicale(
            maladie = maladie,
            date = date,
            dent =  int(dent) if dent else '',
            actes = acte,
            honoraires = honoraire,
            recu = recu,
            reste_a_paye = reste,
            )  # Note: 'reste_a_payer' semble plus approprié que 'reste_a_paye'
        
        items.append(data)
    
    # Enregistrement des objets FicheMedicale
      created_fiches = FicheMedicale.objects.bulk_create(items)
    
      if created_fiches:
         messages.success(request, 'Les données ont été enregistrées avec succès.')
      else:
        messages.error(request, 'Une erreur s\'est données lors de l\'enregistrement des données.')
    
      return render(request, self.template_name) 
    
class visealiserFiche(View):
    template_name = "ficheMedicale.html"
    def get(self, request, *args, **kwargs):
         pk = kwargs.get('pk')
         context = get_context_data(self,pk)

         return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        pk = request.POST.get('pk')
        
        if 'sup' in request.POST:
            try:
                fiche_id = request.POST.get('sup')
                fiche_med = FicheMedicale.objects.get(pk=fiche_id)
                fiche_med.delete()
                messages.success(request, "La suppression a été effectuée avec succès.")
            except ObjectDoesNotExist:
                messages.error(request, "La fiche médicale que vous essayez de supprimer n'existe pas.")
            except Exception as e:
                messages.error(request, f"Désolé, une erreur s'est produite : {e}")
        
        elif 'id_modified' in request.POST:
            try:
                id_fiche = request.POST.get('id_modified')
                fiche = FicheMedicale.objects.get(pk=id_fiche)
                fiche.date = request.POST.get('date')
                fiche.dent = request.POST.get('dent', '')
                fiche.actes = request.POST.get('actes')
                fiche.honoraires = request.POST.get('honoraires','')
                fiche.recu = request.POST.get('recu')
                fiche.reste_a_paye = request.POST.get('reste', '')
                fiche.save()
                messages.success(request, "La modification a été effectuée avec succès.")
            except ObjectDoesNotExist:
                messages.error(request, "La fiche médicale que vous essayez de modifier n'existe pas.")
            except Exception as e:
                messages.error(request, f"Désolé, une erreur s'est produite : {e}")
        
        else:
            try:
                maladie = Maladie.objects.get(pk=pk)
                date = request.POST.get('date')
                dent = request.POST.get('dent', '')
                actes = request.POST.get('actes')
                honoraires = request.POST.get('honoraires')
                recu = request.POST.get('recu')
                reste = request.POST.get('reste', '')

                data = FicheMedicale.objects.create(
                    maladie=maladie,
                    date=date,
                    dent=dent,
                    actes=actes,
                    honoraires=honoraires,
                    recu=recu,
                    reste_a_paye=reste,
                )
                
                if data:
                    messages.success(request, 'Les données ont été enregistrées avec succès.')
                else:
                    messages.error(request, 'Une erreur s\'est produite lors de l\'enregistrement des données.')
            
            except ObjectDoesNotExist:
                messages.error(request, "La maladie spécifiée n'existe pas.")
            except Exception as e:
                messages.error(request, f'Erreur lors de l\'enregistrement des données : {e}')
        
        context = get_context_data(self,pk)
        return render(request, self.template_name, context)
