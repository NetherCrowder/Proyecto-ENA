import datetime

from ..gps import GPS

from ...models import SensorData

def insert_data(data_dict):
    # Generar un tiempo actual
    current_time = datetime.datetime.now()
    
    # Obtener la posición GPS
    gps = GPS()
    gps_data = gps.get_position()
    
    # Agregar timestamp y datos GPS al diccionario
    data_dict['timestamp'] = current_time
    data_dict['gps_lat'] = gps_data['latitude']
    data_dict['gps_lon'] = gps_data['longitude']
    
    # Crear una instancia de SensorData y guardar
    try:
        sensor_data = SensorData.objects.create(**data_dict)
        return sensor_data
    except Exception as e:
        print(f"Error al guardar en la base de datos: {e}")
        return None
