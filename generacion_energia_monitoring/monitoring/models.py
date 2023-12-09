from django.db import models

# Create your models here.

class TipoDispositivo(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre
    
class StatusDispositivo(models.Model):
    descripcion = models.CharField(max_length=255)

    def __str__(self):
        return self.descripcion

class Dispositivo(models.Model):
    nombre = models.CharField(max_length=255)
    tipo_dispositivo = models.ForeignKey(TipoDispositivo, on_delete=models.CASCADE)
    fecha_alta = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    potencia_actual = models.FloatField(null=True, blank=True)
    status_dispositivo = models.ForeignKey(StatusDispositivo, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre
    
class Lectura(models.Model):
    dispositivo = models.ForeignKey(Dispositivo, on_delete=models.CASCADE)
    potencia_actual = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Lectura {self.id} - {self.dispositivo.nombre} - {self.timestamp}"
    
class Mantenimiento(models.Model):
    dispositivo = models.ForeignKey(Dispositivo, on_delete=models.CASCADE)
    fecha_ingreso_mantenimiento = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mantenimiento {self.id} - {self.dispositivo.nombre} - {self.fecha_ingreso_mantenimiento}"