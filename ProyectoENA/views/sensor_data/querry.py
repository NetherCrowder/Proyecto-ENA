from django.http import HttpResponse

from ...services import *

def Consulta(request, top):
    top_data = get_query(top)
    if top_data == "":
        return HttpResponse("No hay datos disponibles")
    return top_data
