from django.contrib import admin
from .models import Task

class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ('created',) # esto sirve para que el campo "created" sea de solo lectura en el admin de Django. De esta manera, no se podrá modificar la fecha de creación de la tarea desde el panel de administración de Django.

# Register your models here.

# este archivo sirve para registrar los modelos en el admin de Django. De esta manera, podremos gestionar los registros desde el panel de administración de Django.

admin.site.register(Task, TaskAdmin)