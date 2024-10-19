import json

from ...services import *

def InsertData(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Crear el diccionario con los datos necesarios
            data_dict = {
                'mag_x': data.get('mag_x'),
                'mag_y': data.get('mag_y'),
                'mag_z': data.get('mag_z'),
                'barometro': data.get('barometro'),
                'ruido': data.get('ruido'),
                'giro_x': data.get('giro_x'),
                'giro_y': data.get('giro_y'),
                'giro_z': data.get('giro_z'),
                'acel_x': data.get('acel_x'),
                'acel_y': data.get('acel_y'),
                'acel_z': data.get('acel_z'),
                'vibracion': data.get('vibracion'),
                # 'timestamp', 'gps_lat' y 'gps_lon' se agregan en insert_data
            }
            
            # Validar que todos los campos necesarios están presentes
            missing_fields = [field for field in data_dict if data_dict[field] is None]
            if missing_fields:
                return JsonResponse({'status': 'error', 'message': f'Campos faltantes: {", ".join(missing_fields)}'}, status=400)
            
            # Llama a la función para insertar los datos en la base de datos
            result = insert_data(data_dict)
            
            if result is not None:
                return JsonResponse({'status': 'success', 'message': 'Data inserted successfully.'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Failed to insert data.'}, status=500)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data.'}, status=400)
        except Exception as e:
            print(f"Error en InsertData: {e}")
            return JsonResponse({'status': 'error', 'message': 'An error occurred.'}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)
