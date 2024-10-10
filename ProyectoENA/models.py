from django.db import models
from db_connection import *
from django.http import JsonResponse
# Create your models here.

class DB_Conexion():
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