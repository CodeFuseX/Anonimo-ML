from os import name
from django.urls import path
from doctorapp import views



urlpatterns = [
    #path(' ',views.doctorhome, name='doctorhome'),
    path('', views.doctorHome, name='doctoranonym'),
    path('docAnonym/', views.doctoranonym, name='doctoranonym'),
    path('pdf/<int:id>/',views.user_report, name="user-pdf-view"),
    path('docsessions/',views.docsession, name="docsessions"),
    path('startsession/<int:id>/', views.startsession, name="startsessions"),
    path('usersession', views.usersession, name="usersession"),
    path('getDetails', views.getDetails, name="getDetails"),
    path('report',views.report, name="report"),
    path('viewReports/<int:id>', views.viewReport, name="viewReport")

]