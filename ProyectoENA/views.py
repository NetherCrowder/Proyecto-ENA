from django.shortcuts import render
from .models import DB_Conexion
from django.http import Http404, HttpResponse, JsonResponse

# Create your views here.
def Login(request):
    return render(request, 'templates/login.html')

def Indicadores(request):
    return render(request, 'templates/vistaIndicadores.html')

def Mapa(request):
    return render(request, 'templates/mapa.html') 

def Variables(request):
    return render(request, 'templates/monitoreoVariables.html') 

def Consulta(request, top):
    top_data = DB_Conexion.get_query(top)
    try:
        if top_data is None or not top_data:
            raise Http404()
    except Http404():
        return HttpResponse("No hay datos hay datos en la base de datos")
    return top_data

def GetData(request):
    data = DB_Conexion.get_data()
    return data