from django.shortcuts import render
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns = [
    path('', views.HomeView.as_view(), name="Home"),
    path('add', views.addFicheView.as_view(), name="add"),
    path('view/<int:pk>', views.visealiserFiche.as_view(), name="view"),
    


]