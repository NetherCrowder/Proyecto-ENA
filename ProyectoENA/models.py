from django.db import models
from db_connection import *
from django.http import JsonResponse
import datetime
import geocoder
import random
from geopy import distance  # Asegúrate de tener instalado el paquete geopy
# Create your models here.

class DB_Conexion():    
    def insert_data(mag_x, mag_y, mag_z,barometro,ruido, giro_x, giro_y, giro_z, acel_x, acel_y, acel_z, vibracion):
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
                INSERT INTO sensor_data (timestamp, mag_x, mag_y, mag_z, barometro, ruido, 
                                        giro_x, giro_y, giro_z, acel_x, acel_y, acel_z, 
                                        vibracion, gps_lat, gps_lon)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (current_time, new_data['magnetometro']['x'], new_data['magnetometro']['y'], 
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

class GPS:
    def __init__(self):
        # Obtener la posición actual del dispositivo
        g = geocoder.ip('me')  # Obtiene la ubicación basada en la IP
        self.center_lat, self.center_lon = g.latlng  # Extrae latitud y longitud
        self.speed = 0  # Inicializa velocidad a 0
        self.bearing = 0  # Inicializa dirección a 0
        self.max_distance = 5  # km, distancia máxima desde el centro

    def update_position(self):
        # Actualiza la latitud y longitud con datos reales
        new_lat = self.center_lat  # Usar el valor actual
        new_lon = self.center_lon  # Usar el valor actual
        new_speed = self.speed  # Usar la velocidad actual
        new_bearing = self.bearing  # Usar la dirección actual

        # Calcula el nuevo punto basado en la velocidad y dirección
        origin = (self.center_lat, self.center_lon)
        distance_meters = new_speed  # Suponiendo que la velocidad está en m/s
        destination = distance.distance(meters=distance_meters).destination(origin, new_bearing)

        new_lat, new_lon = destination.latitude, destination.longitude

        # Verifica si el nuevo punto está dentro del radio permitido
        if distance.distance((self.center_lat, self.center_lon), (new_lat, new_lon)).km <= self.max_distance:
            self.center_lat, self.center_lon = new_lat, new_lon
        else:
            # Si está fuera del radio, genera un nuevo punto aleatorio dentro del área permitida
            angle = random.uniform(0, 360)  # Genera un ángulo aleatorio
            dist = random.uniform(0, self.max_distance)  # Genera una distancia aleatoria
            new_point = distance.distance(kilometers=dist).destination((self.center_lat, self.center_lon), angle)
            self.center_lat, self.center_lon = new_point.latitude, new_point.longitude

    def get_position(self):
        self.update_position()
        data = {
            'latitude': self.center_lat,
            'longitude': self.center_lon,
            'speed': self.speed,
            'bearing': self.bearing
        }
        return data