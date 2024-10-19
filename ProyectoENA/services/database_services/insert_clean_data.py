import datetime

from ..gps import GPS

from ...models import SensorDataClean

def insert_clean_data(data_dict):
    try:
        gps = GPS()
        gps_data = gps.get_position()

        data_dict['timestamp'] = datetime.datetime.now()
        data_dict['gps_lat'] = gps_data['latitude']
        data_dict['gps_lon'] = gps_data['longitude']

        # Crear una instancia de SensorDataClean y guardar
        _ = SensorDataClean.objects.create(**data_dict)
        return data_dict
    except Exception as e:
        print(f"Error al guardar en la base de datos: {e}")
        return None