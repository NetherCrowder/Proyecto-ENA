import datetime
import pandas as pd

from django.http import JsonResponse

from .gps import GPS
from .db_connection import *

from ..models import *


class DB_Conexion():    
    def insert_data(mag_x, mag_y, mag_z,barometro,ruido, giro_x, giro_y, giro_z, acel_x, acel_y, acel_z, vibracion, table = 'sensor_data'):
        #mag_x = float(0.0)
        #mag_y = float(0.0)
        #mag_z = float(0.0)
        #barometro = float(0.0)
        #ruido = float(0.0)
        #giro_x = float(0.0)
        #giro_y = float(0.0)
        #giro_z = float(0.0)
        #acel_x = float(0.0)
        #acel_y = float(0.0)
        #acel_z = float(0.0)
        #vibracion = float(0.0)

         # Generar un tiempo actual en formato ISO
        current_time = datetime.datetime.now()
        
        # Obtener la posición GPS
        gps = GPS()
        gps_data = gps.get_position()
        
        # Generar datos aleatorios para todas las mediciones
        new_data = {
            'timestamp': current_time,
            'magnetometro': {
                'x': mag_x,
                'y': mag_y,
                'z': mag_z
            },
            'barometro': barometro,
            'ruido': ruido,
            'giroscopio': {
                'x': giro_x,
                'y': giro_y,
                'z': giro_z
            },
            'acelerometro': {
                'x': acel_x,
                'y': acel_y,
                'z': acel_z
            },
            'vibracion': vibracion,
            'gps': {
                'latitud': gps_data['latitude'],
                'longitud': gps_data['longitude']
            }
        }
        
        # Guardar datos en la base de datos
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO ? (timestamp, mag_x, mag_y, mag_z, barometro, ruido, 
                                        giro_x, giro_y, giro_z, acel_x, acel_y, acel_z, 
                                        vibracion, gps_lat, gps_lon)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (table, current_time, new_data['magnetometro']['x'], new_data['magnetometro']['y'], 
                new_data['magnetometro']['z'], new_data['barometro'], new_data['ruido'],
                new_data['giroscopio']['x'], new_data['giroscopio']['y'], new_data['giroscopio']['z'],
                new_data['acelerometro']['x'], new_data['acelerometro']['y'], new_data['acelerometro']['z'],
                new_data['vibracion'], new_data['gps']['latitud'], new_data['gps']['longitud']))
            conn.commit()
        except Exception as e:
            return(f"Error al guardar en la base de datos: {e}")
        finally:
            if conn:
                conn.close()
        return new_data
    
    def insert_clean_data(data_dict):
        try:
            gps = GPS()
            gps_data = gps.get_position()

            data_dict['timestamp'] = datetime.datetime.now()
            data_dict['gps_lat'] = gps_data['latitude']
            data_dict['gps_lon'] = gps_data['longitude']

            # Crear una instancia del modelo y guardar
            sensor_data = SensorDataClean(**data_dict)
            sensor_data.save()
            return data_dict
        except Exception as e:
            print(f"Error al guardar en la base de datos: {e}")
            return None

    def get_data():
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            # Obtener los últimos 100 registros
            cursor.execute("""
                SELECT timestamp, mag_x, mag_y, mag_z, barometro, ruido, 
                    giro_x, giro_y, giro_z, acel_x, acel_y, acel_z, 
                    vibracion, gps_lat, gps_lon
                FROM sensor_data
                WHERE timestamp = (SELECT MAX(timestamp) FROM sensor_data)
            """)
            rows = cursor.fetchall()
            # Convertir los resultados a un formato JSON
            data = []
            for row in rows:
                data.append({
                    'timestamp': row.timestamp.isoformat(),
                    'magnetometro': {
                        'x': row.mag_x,
                        'y': row.mag_y,
                        'z': row.mag_z
                    },
                    'barometro': row.barometro,
                    'ruido': row.ruido,
                    'giroscopio': {
                        'x': row.giro_x,
                        'y': row.giro_y,
                        'z': row.giro_z
                    },
                    'acelerometro': {
                        'x': row.acel_x,
                        'y': row.acel_y,
                        'z': row.acel_z
                    },
                    'vibracion': row.vibracion,
                    'gps': {
                        'latitud': row.gps_lat,
                        'longitud': row.gps_lon
                    }
                })
            return JsonResponse(data, safe=False)
        except Exception as e:
            print(f"Error al obtener datos de la base de datos: {e}")
            return JsonResponse({"error": "No se pudieron obtener los datos"}, safe=False), 500
        finally:
            if conn:
                conn.close()
                
    def get_data_as_dataframe():
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            # Obtener los últimos 100 registros
            cursor.execute("""
                SELECT timestamp, mag_x, mag_y, mag_z, barometro, ruido, 
                    giro_x, giro_y, giro_z, acel_x, acel_y, acel_z, 
                    vibracion, gps_lat, gps_lon
                FROM sensor_data
            """)
            rows = cursor.fetchall()
            # Convertir los resultados a un formato JSON
            data = []
            for row in rows:
                data.append({
                    'timestamp': row.timestamp.isoformat(),
                    'mag_x': row.mag_x,
                    'mag_y': row.mag_y,
                    'mag_z': row.mag_z,
                    'barometro': row.barometro,
                    'ruido': row.ruido,
                    'giro_x': row.giro_x,
                    'giro_y': row.giro_y,
                    'giro_z': row.giro_z,
                    'acel_x': row.acel_x,
                    'acel_y': row.acel_y,
                    'acel_z': row.acel_z,
                    'vibracion': row.vibracion,
                    'gps_lat': row.gps_lat,
                    'gps_lon': row.gps_lon
                })
            df = pd.DataFrame(data)
            return df
        except Exception as e:
            print(f"Error al obtener datos de la base de datos: {e}")
            return JsonResponse({"error": "No se pudieron obtener los datos"}, safe=False), 500
        finally:
            if conn:
                conn.close()
    
    def get_query(query):
        conn = get_db_connection()
        cursor = conn.cursor()        
        cursor.execute("""SELECT TOP """f"{query}"""" * FROM sensor_data""")
        rows = cursor.fetchall()
        if rows is None or not rows:
            return ("")
        else:
            column_names = [description[0] for description in cursor.description]
            data = [dict(zip(column_names, row)) for row in rows]
            return JsonResponse(data, safe=False)

    def autenticar_usuario(username, password):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            # Consultar el usuario y la contraseña
            cursor.execute("""
                SELECT * FROM users WHERE username = '"""f"{username}'" """ AND password = '"""f"{password}'""")
            print(cursor)
            user = cursor.fetchone()
            if user:
                return JsonResponse({"mensaje": "Autenticación exitosa"}, status=200)
            else:
                return JsonResponse({"error": "Usuario o contraseña incorrectos"}, status=401)
        except Exception as e:
            print(f"Error al autenticar al usuario: {e}")
            return JsonResponse({"error": "Error en la autenticación"}, status=500)
        finally:
            if conn:
                conn.close()