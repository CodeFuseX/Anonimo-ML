from django.urls import path
from doctorapp import views



urlpatterns = [
    #path(' ',views.doctorhome, name='doctorhome'),
    path('', views.doctorHome, name='doctoranonym'),
    path('docAnonym/', views.doctoranonym, name='doctoranonym')

]