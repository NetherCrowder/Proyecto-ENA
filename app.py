from flask import Flask, jsonify, render_template, request
import random
import datetime
import uuid
from geopy import distance
from db_connection import get_db_connection, test_db_connection

Registros = []

app = Flask(__name__)

@app.route('/result')
def result():
    return render_template('result.html')

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/vistaIndicadores')
def vistaIndicadores():
    return render_template('vistaIndicadores.html')

@app.route('/monitoreoVariables')
def monitoreoVariables():
    return render_template('monitoreoVariables.html')

@app.route('/mapa')
def mapa():
    return render_template('mapa.html')

@app.route('/index')
def index():
    return render_template('index.html')  # Sirve la página HTML

@app.route('/historical')
def historical():
    return render_template('historical_data.html')

@app.route('/data')
def data():
    # Generar un tiempo actual en formato ISO
    current_time = datetime.datetime.now()
    
    # Obtener la posición GPS simulada
    gps_data = gps_sim.get_position()
    
    # Generar datos aleatorios para todas las mediciones
    new_data = {
        'timestamp': current_time,
        'magnetometro': {
            'x': random.uniform(-100, 100),
            'y': random.uniform(-100, 100),
            'z': random.uniform(-100, 100)
        },
        'barometro': random.uniform(900, 1100),
        'ruido': random.uniform(30, 120),
        'giroscopio': {
            'x': random.uniform(-180, 180),
            'y': random.uniform(-180, 180),
            'z': random.uniform(-180, 180)
        },
        'acelerometro': {
            'x': random.uniform(-10, 10),
            'y': random.uniform(-10, 10),
            'z': random.uniform(-10, 10)
        },
        'vibracion': random.uniform(0, 10),
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
        print(f"Error al guardar en la base de datos: {e}")
    finally:
        if conn:
            conn.close()
    
    # Agregar los nuevos datos a los registros
    Registros.append(new_data)
    
    # Limitar el número de registros a los últimos 100 para evitar un crecimiento excesivo
    if len(Registros) > 100:
        Registros.pop(0)
    
    return jsonify(Registros)

@app.route('/location_data')
def location_data():
    # Generar un tiempo actual en formato ISO
    current_time = datetime.datetime.now().isoformat()
    
    # Generar datos aleatorios para los campos especificados
    new_location_data = {
        'id': str(uuid.uuid4()),  # Genera un ID único
        'timestamp': current_time,
        'latitude': random.uniform(-90, 90),
        'longitude': random.uniform(-180, 180),
        'altitude': random.uniform(0, 8848),  # Altura máxima del Monte Everest
        'speed': random.uniform(0, 120),  # Velocidad en km/h
        'angle': random.uniform(0, 360),  # Ángulo en grados
        'acceleration': {
            'x': random.uniform(-20, 20),
            'y': random.uniform(-20, 20),
            'z': random.uniform(-20, 20)
        },
        'distance': random.uniform(0, 1000),  # Distancia en metros
        'user_id': str(uuid.uuid4())  # Genera un ID de usuario aleatorio
    }
    
    return jsonify(new_location_data)

class GPSSimulator:
    def __init__(self, start_lat, start_lon):
        self.lat = start_lat
        self.lon = start_lon
        self.speed = random.uniform(0, 5)  # m/s, velocidad más realista para una ciudad
        self.bearing = random.uniform(0, 360)  # grados
        self.center_lat, self.center_lon = 6.2442, -75.5812  # Centro de Medellín
        self.max_distance = 5  # km, distancia máxima desde el centro

    def update_position(self):
        # Calcula el nuevo punto basado en velocidad y dirección
        origin = distance.distance(meters=self.speed)
        destination = origin.destination((self.lat, self.lon), self.bearing)
        new_lat, new_lon = destination.latitude, destination.longitude

        # Verifica si el nuevo punto está dentro del radio permitido
        if distance.distance((self.center_lat, self.center_lon), (new_lat, new_lon)).km <= self.max_distance:
            self.lat, self.lon = new_lat, new_lon
        else:
            # Si está fuera del radio, genera un nuevo punto aleatorio dentro del área permitida
            angle = random.uniform(0, 360)
            dist = random.uniform(0, self.max_distance)
            new_point = distance.distance(kilometers=dist).destination((self.center_lat, self.center_lon), angle)
            self.lat, self.lon = new_point.latitude, new_point.longitude

        # Actualiza velocidad y dirección aleatoriamente
        self.speed += random.uniform(-0.5, 0.5)  # Cambia velocidad gradualmente
        self.speed = max(0, min(self.speed, 10))  # Limita entre 0 y 10 m/s
        self.bearing += random.uniform(-10, 10)  # Cambia dirección gradualmente

    def get_position(self):
        self.update_position()
        return {
            'latitude': self.lat,
            'longitude': self.lon,
            'speed': self.speed,
            'bearing': self.bearing
        }

# Inicializa el simulador con una posición de inicio
gps_sim = GPSSimulator(6.2442, -75.5812)  # Ejemplo: Nueva York

@app.route('/gps_data')
def gps_data():
    return jsonify(gps_sim.get_position())

@app.route('/db_status')
def db_status():
    if test_db_connection():
        return jsonify({"status": "Conexión a la base de datos exitosa"}), 200
    else:
        return jsonify({"status": "Error de conexión a la base de datos"}), 500

@app.route('/get_data')
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
        
        return jsonify(data)
    
    except Exception as e:
        print(f"Error al obtener datos de la base de datos: {e}")
        return jsonify({"error": "No se pudieron obtener los datos"}), 500
    
    finally:
        if conn:
            conn.close()

def select(query):
    conn = get_db_connection()
    cursor = conn.cursor()        
    # Obtener los últimos 100 registros
    cursor.execute("""SELECT TOP """f"{query}"""" * FROM sensor_data""")

    rows = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]
    data = [dict(zip(column_names, row)) for row in rows]

    return data

@app.route('/consultaSQL/', methods=['GET'])
def consulta_sql():
    query = request.args.get('')
    if not query:
        return render_template('monitoreoVariables.html')

    try:
        data = select(query)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    if test_db_connection():
        print("La aplicación se ha iniciado con una conexión exitosa a la base de datos.")
        app.run(debug=True)
    else:
        print("No se pudo establecer la conexión a la base de datos. La aplicación no se iniciará.")