from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import DB, Question, Choice
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.db.models import F
from django.urls import reverse


def index1(request):
    sensor_data = DB.get_db()
    output = ", ".join([str(q['id']) for q in sensor_data])
    return HttpResponse(output)

def index2(request):
    sensor_data = DB.get_db()  # Cambié el nombre para reflejar que son datos de sensores
    template = loader.get_template("test/index.html")
    context = {
        "sensor_data": sensor_data,  # Cambié el nombre aquí también
    }
    return HttpResponse(template.render(context, request))

def index3(request):
    sensor_data = DB.get_db(1)
    context = {"sensor_data": sensor_data}
    return render(request, "test/index.html", context)

def index_detail(request, id):
    sensor_data = DB.get_db(id)
    try:
        if sensor_data is None or not sensor_data:
            raise Http404()
    except Http404 as e:
        return HttpResponse("No se encontraron datos para el "+str(id)+" proporcionado.", status=404)
    #except Exception as e:
    #    return HttpResponse("Ocurrió un error: " + str(e), status=500)  # Maneja otras excepciones
    return render(request, "test/index.html", {"sensor_data": sensor_data})

def index_detail2(request, id):
    sensor_data = DB.get_db(id)
    try:
        if sensor_data is None or not sensor_data:
            raise Http404()
    except Http404:
        return HttpResponse("No se encontraron datos para el "+str(id)+" proporcionado.", status=404)
    else:
        data = next((item for item in sensor_data if item['id'] == id), None)
        #return render(request, "test/detail.html", {"sensor_data": sensor_data})
        return HttpResponseRedirect(reverse("test:results", args=(data["id"],)))  # Asegúrate de pasar solo el ID
    

def detail(request, question_id):
   return HttpResponse("You're looking at question %s." % question_id)


def results(request, id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)  
# Create your views here.

