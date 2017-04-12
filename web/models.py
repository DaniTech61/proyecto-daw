from django.db import models
from django.utils import timezone

class Local(models.Model):
	nombreLocal = models.CharField(primary_key=True,max_length=15)
	direccion = models.CharField(max_length=60)
	descripcion = models.TextField()
	imagen = models.CharField(max_length=60)
	CATEGORIAS_LOCALES = (
		('copas', 'Copas'),
		('noche', 'Noche'),
		('comer', 'Comer'),
		('tapeo', 'Tapas'),
		('dulce', 'Dulce'),
		('varios', 'Varios'),
	)
	categoria = models.CharField(max_length=10, choices=CATEGORIAS_LOCALES, default='varios')
	fechaAlta = models.DateTimeField(default=timezone.now)
	def alta(self):
		self.fechaAlta = timezone.now()
		self.save()
		
class Turismo(models.Model):
	nombreSitio =  models.CharField(primary_key=True,max_length=30)
	direccion = models.CharField(max_length=60)
	descripcion = models.TextField()
	imagen = models.CharField(max_length=60)
	CATEGORIAS_TURISMO = (
		('fuente', 'Fuente'),
		('parque', 'Parque'),
		('museo', 'Museo'),
		('teatro', 'Teatro'),
		('auditorio', 'Auditorio'),	
		('puerta', 'Puerta'),
		('otros', 'Otros'),
	)
	categoria = models.CharField(max_length=15, choices=CATEGORIAS_TURISMO, default='otros')
	fechaAlta = models.DateTimeField(default=timezone.now)
	def alta(self):
		self.fechaAlta = timezone.now()
		self.save()
		
class Comentarios(models.Model):
	autor = models.ForeignKey('auth.User',on_delete=models.CASCADE)
	local = models.ForeignKey('Local',on_delete=models.CASCADE)
	titulo = models.CharField(max_length=50)
	comentario = models.TextField()
	fecha_publicacion = models.DateTimeField(
			blank=True, null=True)
	def publish(self):
		self.fecha_publicacion = timezone.now()
		self.save()