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
    path('GetUsers/<str:username>&<str:password>/', views.GetUsers, name='GetUsers'),
    path('InsertData/<str:mag_x>/<str:mag_y>/<str:mag_z>/<str:barometro>/<str:ruido>/<str:giro_x>/<str:giro_y>/<str:giro_z>/<str:acel_x>/<str:acel_y>/<str:acel_z>/<str:vibracion>/', views.InsertData, name='InsertData'),
    path('test', views.test),
]
