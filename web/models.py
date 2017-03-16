from django.db import models
from django.utils import timezone

class Local(models.Model):
	nombreLocal = models.CharField(primary_key=True,max_length=15)
	direccion = models.CharField(max_length=60)
	descripcion = models.TextField()
	imagen = models.CharField(max_length=60)
	fechaAlta = models.DateTimeField(default=timezone.now)
	def alta(self):
		self.fechaAlta = timezone.now()
		self.save()