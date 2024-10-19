from django.urls import path

from . import views
from . import constants

app_name = 'ProyectoENA'

urlpatterns = [
    path(constants.LOGIN, views.Login, name='Login'),
    path(constants.CLEAN_DATA, views.CleanData, name='Clean Data'),
    path(constants.GET_DATA, views.GetData, name='GetData'),
    path(f'{constants.GET_USERS}/<str:username>&<str:password>/', views.GetUsers, name='GetUsers'),
    path(constants.INDICATORS, views.Indicadores, name='Indicadores'),
    path(f'{constants.INSERT_DATA}?<str:mag_x>/<str:mag_y>/<str:mag_z>/<str:barometro>/<str:ruido>/<str:giro_x>/<str:giro_y>/<str:giro_z>/<str:acel_x>/<str:acel_y>/<str:acel_z>/<str:vibracion>/',
         views.InsertData,
         name='InsertData'),
    path(constants.MAP, views.Mapa, name='Mapa'),
    path(constants.VARIABLES, views.Variables, name='Variables'),
    path(f'{constants.VARIABLES}/<int:top>', views.Consulta, name='Consulta'),
]
