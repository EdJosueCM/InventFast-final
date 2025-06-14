# core/context_processors.py

from .models import Producto
from datetime import timedelta
from django.utils import timezone

def notificaciones_context(request):
    notificaciones = []

    productos_bajo_stock = Producto.objects.filter(cantidad__lt=20, activo=True)
    for prod in productos_bajo_stock:
        notificaciones.append(f"⚠️ Stock bajo: {prod.nombre} ({prod.cantidad} unidades)")

    productos_inactivos = Producto.objects.filter(activo=False)
    for prod in productos_inactivos:
        notificaciones.append(f"❌ Producto inactivo: {prod.nombre}")

    # Nuevos productos (últimos 2 días)
    nuevos = Producto.objects.filter(fecha_ingreso__gte=timezone.now() - timedelta(days=2))
    for prod in nuevos:
        notificaciones.append(f"🆕 Producto agregado: {prod.nombre}")

    # Productos eliminados (si usas soft-delete puedes añadir lógica aquí)

    # Invertir para que salgan las más recientes primero
    notificaciones.reverse()

    return {"notificaciones": notificaciones}
