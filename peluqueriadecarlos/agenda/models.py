from django.db import models, transaction
from django.db.models import F, Max
from datetime import datetime

import hashlib

""" class Cliente(models.Model):
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
        return f"{self.hora or ''} {self.fecha or ''}".strip() """
        


# class Cliente(models.Model):
#     nombre = models.CharField(max_length=100)
#     telefono = models.CharField(max_length=10)
#     fecha = models.DateField()
#     hora = models.TimeField()
#     estado = models.CharField(
#         max_length=20,
#         choices=[('Pendiente', 'Pendiente'), ('Proceso', 'En Proceso'), ('Completado', 'Completado')],
#         default='Pendiente'
#     )
#     turno = models.PositiveIntegerField(unique=True)
#     token = models.CharField(max_length=64, blank=True, unique=True)  # Nuevo campo para el token

#     def generate_token(self):
#         """Genera un token único basado en el número de teléfono y el turno"""
#         if self.telefono and self.turno:
#             # Combina el teléfono con el turno y una salt para mayor unicidad
#             salt = "CarlosBarberShop2025"  # Cambia esto por una salt segura
#             token_string = f"{self.telefono}{self.turno}{salt}"
#             # Genera un hash SHA-256 del token_string
#             token = hashlib.sha256(token_string.encode()).hexdigest()
#             return token
#         return None

#     def save(self, *args, **kwargs):
#         # Genera y asigna el token antes de guardar
#         if not self.token:
#             self.token = self.generate_token()
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"{self.nombre} - {self.fecha} {self.hora}"


# class HorarioNoDisponible(models.Model):
#     hora = models.TimeField(null=True, blank=True)
#     fecha = models.DateField(null=True, blank=True)

#     def __str__(self):
#         return f"{self.hora or ''} {self.fecha or ''}".strip()






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
    turno = models.PositiveIntegerField(unique=True)
    token = models.CharField(max_length=64, blank=True, unique=True)

    def generate_token(self):
        if self.telefono and self.turno:
            salt = "CarlosBarberShop2025"
            token_string = f"{self.telefono}{self.turno}{salt}"
            token = hashlib.sha256(token_string.encode()).hexdigest()
            return token
        return None

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = self.generate_token()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre} - {self.fecha} {self.hora}"

class HorarioNoDisponible(models.Model):
    hora = models.TimeField(null=True, blank=True)
    fecha = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.hora or ''} {self.fecha or ''}".strip()