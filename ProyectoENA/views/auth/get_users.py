from ...services import *

def GetUsers(request, username, password):
    print(username)
    data = autenticar_usuario(username, password)
    return data
