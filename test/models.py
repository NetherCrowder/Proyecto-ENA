from django.db import models
from db_connection import *
from django.http import JsonResponse
# Create your models here.

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")
    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text
    
class DB():
    def get_db(query):
        conn = get_db_connection()
        cursor = conn.cursor()        
        # Obtener los últimos 100 registros
        #cursor.execute("""SELECT * FROM sensor_data Where Id = """f"{query}""")
        cursor.execute("""SELECT * FROM sensor_data""")
        #cursor.execute("""select * from sensor_data where id = 5003""")

        rows = cursor.fetchall()
        column_names = [description[0] for description in cursor.description]
        data = [dict(zip(column_names, row)) for row in rows]

        return data
    
    def test_db():
        if test_db_connection():
            return ({"status": "Conexión a la base de datos exitosa"}), 200
        else:
            return ({"status": "Error de conexión a la base de datos"}), 500
