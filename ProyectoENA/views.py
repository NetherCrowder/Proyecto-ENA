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
    print((top_data))
    try:
        if top_data is "":
            raise Http404  # Cambié esto para evitar el error
    except Http404:
        return HttpResponse("No hay datos disponibles")
    return HttpResponse(top_data)

def GetData(request):
    data = DB_Conexion.get_data()
    return data