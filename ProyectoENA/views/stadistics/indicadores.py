from django.shortcuts import render


def Indicadores(request):
    # Puedes agregar lógica aquí si es necesario
    return render(request, 'stadistics/vistaIndicadores.html')