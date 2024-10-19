from django.db import models

class SensorData(models.Model):
    timestamp = models.DateTimeField()
    mag_x = models.FloatField()
    mag_y = models.FloatField()
    mag_z = models.FloatField()
    barometro = models.FloatField()
    ruido = models.FloatField()
    giro_x = models.FloatField()
    giro_y = models.FloatField()
    giro_z = models.FloatField()
    acel_x = models.FloatField()
    acel_y = models.FloatField()
    acel_z = models.FloatField()
    vibracion = models.FloatField()
    gps_lat = models.FloatField()
    gps_lon = models.FloatField()

    class Meta:
        db_table = 'sensor_data'  # Especifica el nombre de la tabla si es diferente al nombre del modelo
