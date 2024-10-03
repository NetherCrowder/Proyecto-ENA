from django.urls import path
from . import views

app_name = 'ProyectoENA'

urlpatterns = [
    path('', views.Login, name='Login'),
    path('Indicadores', views.Indicadores, name='Indicadores'),
    path('Variables', views.Variables, name='Variables'),
    path('Mapa', views.Mapa, name='Mapa'),
    path('Indicadores/<int:top>', views.Consulta, name='Consulta'),
    path('GetData', views.GetData, name='GetData'),
]