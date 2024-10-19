import geocoder
import random
from geopy import distance

class GPS:
    def __init__(self):
        try:
            # Obtener la posición actual del dispositivo
            g = geocoder.ip('me')  # Obtiene la ubicación basada en la IP
            if g.latlng:
                self.center_lat, self.center_lon = g.latlng  # Extrae latitud y longitud
            else:
                print("No se pudo obtener la ubicación basada en la IP.")
                # Establecer valores predeterminados o manejar el error
                self.center_lat = 0.0  # Reemplaza con una latitud predeterminada
                self.center_lon = 0.0  # Reemplaza con una longitud predeterminada
        except Exception as e:
            print(f"Error al obtener la ubicación: {e}")
            # Establecer valores predeterminados o manejar el error
            self.center_lat = 0.0
            self.center_lon = 0.0
        self.speed = 0  # Inicializa velocidad a 0
        self.bearing = 0  # Inicializa dirección a 0
        self.max_distance = 5  # km, distancia máxima desde el centro

    def update_position(self):
        # Actualiza la latitud y longitud con datos reales o simulados
        new_lat = self.center_lat
        new_lon = self.center_lon
        new_speed = self.speed
        new_bearing = self.bearing

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
            angle = random.uniform(0, 360)  # Ángulo aleatorio en grados
            dist = random.uniform(0, self.max_distance * 1000)  # Distancia aleatoria en metros
            new_point = distance.distance(meters=dist).destination((self.center_lat, self.center_lon), angle)
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
