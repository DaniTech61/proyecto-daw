from django.contrib import admin
from .models import Local
from .models import Turismo
from .models import Comentarios
from .models import Valoracion

admin.site.register(Local)
admin.site.register(Turismo)
admin.site.register(Comentarios)
admin.site.register(Valoracion)