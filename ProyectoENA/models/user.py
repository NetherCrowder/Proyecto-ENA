from django.db import models

class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)  # Considera almacenar contraseñas hash
    # Otros campos...

    class Meta:
        db_table = 'users'
