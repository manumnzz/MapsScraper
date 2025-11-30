from django.db import models

class Business(models.Model):
    nombre = models.CharField(max_length=255)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    telefono = models.CharField(max_length=50, blank=True, null=True)
    rating = models.FloatField(null=True, blank=True)
    categoria = models.CharField(max_length=255, blank=True, null=True)
    ciudad = models.CharField(max_length=100, blank=True, null=True)
    web = models.CharField(max_length=255, blank=True, null=True)
    fecha_scraping = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre