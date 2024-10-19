from django.contrib.auth import authenticate
from django.http import JsonResponse

from ...models import User

def autenticar_usuario(username, password):
    try:
        user = User.objects.get(username=username, password=password)
        if user:
            return JsonResponse({"mensaje": "Autenticación exitosa"}, status=200)
        else:
            return JsonResponse({"error": "Usuario o contraseña incorrectos"}, status=401)
    except User.DoesNotExist:
        return JsonResponse({"error": "Usuario o contraseña incorrectos"}, status=401)
    except Exception as e:
        print(f"Error al autenticar al usuario: {e}")
        return JsonResponse({"error": "Error en la autenticación"}, status=500)

