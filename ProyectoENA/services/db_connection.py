import pyodbc
import logging

# Configuración del logging
logging.basicConfig(filename='db_connection.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

# Configuración de la conexión a la base de datos
SERVER = 'LAPTOP-32A7LDRB\SQLEXPRESS'
DATABASE = 'test'
USERNAME = 'Aaron'
PASSWORD = ''

# Cadena de conexión
connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}'

def get_db_connection():
    try:
        conn = pyodbc.connect(connection_string)
        return conn
    except Exception as e:
        logging.error(f"Error al conectar a la base de datos: {e}")
        raise

def test_db_connection():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT @@version;")
        db_version = cursor.fetchone()
        logging.info(f"Conexión exitosa. Versión de la base de datos: {db_version[0]}")
        conn.close()
        return True
    except Exception as e:
        logging.error(f"Error al probar la conexión a la base de datos: {e}")
        return False

#if __name__ == "__main__":
#    if test_db_connection():
#        print("La conexión a la base de datos es exitosa.")
#    else:
#        print("No se pudo establecer la conexión a la base de datos. Verifica la configuración.")