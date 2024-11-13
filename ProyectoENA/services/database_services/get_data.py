import pandas as pd

from django.http import JsonResponse

from ...models import SensorData

def get_data():
    try:
        # Obtener el último registro
        latest_data = SensorData.objects.latest('timestamp')

        print(latest_data.barometro)
        
        data = {
            'timestamp': latest_data.timestamp.isoformat(),
            'magnetometro': {
                'x': latest_data.mag_x,
                'y': latest_data.mag_y,
                'z': latest_data.mag_z
            },
            'barometro': latest_data.barometro,
            'ruido': latest_data.ruido,
            'giroscopio': {
                'x': latest_data.giro_x,
                'y': latest_data.giro_y,
                'z': latest_data.giro_z
            },
            'acelerometro': {
                'x': latest_data.acel_x,
                'y': latest_data.acel_y,
                'z': latest_data.acel_z
            },
            'vibracion': latest_data.vibracion,
            'gps': {
                'latitud': latest_data.gps_lat,
                'longitud': latest_data.gps_lon
            }
        }
        return JsonResponse(data, safe=False)
    except SensorData.DoesNotExist:
        return JsonResponse({"error": "No se encontraron datos"}, status=404)
    except Exception as e:
        print(f"Error al obtener datos de la base de datos: {e}")
        return JsonResponse({"error": "No se pudieron obtener los datos"}, status=500)
    

def get_data_as_dataframe():
    try:
        data = SensorData.objects.all().values(
            'timestamp', 'mag_x', 'mag_y', 'mag_z', 'barometro', 'ruido',
            'giro_x', 'giro_y', 'giro_z', 'acel_x', 'acel_y', 'acel_z',
            'vibracion', 'gps_lat', 'gps_lon'
        )
        df = pd.DataFrame(list(data))
        return df
    except Exception as e:
        print(f"Error al obtener datos de la base de datos: {e}")
        return None  # o maneja la excepción según sea necesario

