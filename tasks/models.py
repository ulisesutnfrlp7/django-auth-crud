from django.db import models

# Create your models here.

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE) # esto sirve para relacionar cada tarea con un usuario específico. De esta manera, cada usuario solo podrá ver y gestionar sus propias tareas.

    def __str__(self): # El constructor sirve para mostrar el título de la tarea en lugar de "Task object (1)" cuando se muestre la tarea en el admin de Django o en la consola de Python.
        return self.title