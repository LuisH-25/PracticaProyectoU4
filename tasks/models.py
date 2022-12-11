from django.db import models

from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)  # si no pasa nada, por defecto estara vacio
    created = models.DateTimeField(auto_now_add=True)   # anhade la fecha por defecto
    datecompleted = models.DateTimeField(null=True, blank=True)     # inicialmente es null, se acepta vacio
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)    # si se elimina el usuario, se elimina las tareas

    def __str__(self):
        return self.title + " -by " + self.user.username
