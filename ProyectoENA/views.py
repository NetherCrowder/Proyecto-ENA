from django.shortcuts import render
from .models import DB_Conexion, GPS
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

def GetUsers(request, username, password):
    data = DB_Conexion.autenticar_usuario(username, password)
    return data

def InsertData(request, mag_x, mag_y, mag_z, barometro, ruido, giro_x, giro_y, giro_z, acel_x, acel_y, acel_z, vibracion):
    if request.method == 'POST':
        # Aquí puedes procesar los datos como desees
        # Por ejemplo, puedes imprimirlos o usarlos directamente
        #print(f"Received data: {mag_x}, {mag_y}, {mag_z}, {barometro}, {ruido}, {giro_x}, {giro_y}, {giro_z}, {acel_x}, {acel_y}, {acel_z}, {vibracion}")

        # Llama a la función para insertar los datos en la base de datos
        result = DB_Conexion.insert_data(mag_x, mag_y, mag_z, barometro, ruido, giro_x, giro_y, giro_z, acel_x, acel_y, acel_z, vibracion)

        # Asegúrate de que result sea un valor que puedas convertir a JSON
        if result is None:
            return JsonResponse({'status': 'success', 'message': 'Data inserted successfully.'})
        else:
            return JsonResponse({'status': 'success', 'message': result})  # Asegúrate de que result sea un string o un objeto JSON válido
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)
    
def test(request):
    return render(request, 'templates/post.html')
