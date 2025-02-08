from django.db import models, transaction
from django.db.models import F, Max
from datetime import datetime

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=10)
    fecha = models.DateField()
    hora = models.TimeField()
    estado = models.CharField(
        max_length=20,
        choices=[('Pendiente', 'Pendiente'), ('Proceso', 'En Proceso'), ('Completado', 'Completado')],
        default='Pendiente'
    )
    turno = models.PositiveIntegerField(unique=True)  # Garantiza que los turnos no se repitan

    def __str__(self):
        return f"{self.nombre} - {self.fecha} {self.hora}"







class HorarioNoDisponible(models.Model):
    hora = models.TimeField(null=True, blank=True)  # Campo para horas
    fecha = models.DateField(null=True, blank=True)  # Campo para fechas

    def __str__(self):
        return f"{self.hora or ''} {self.fecha or ''}".strip()