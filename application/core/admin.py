from django.contrib import admin

# Register your models here.
from .models import *
# Register your models here.
admin.site.register(Factura)
admin.site.register(FacturaDetalle)
admin.site.register(Producto)