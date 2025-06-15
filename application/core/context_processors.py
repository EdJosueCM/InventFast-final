# core/context_processors.py

from datetime import timedelta
from django.utils import timezone
from .models import Producto, Carrito

def notificaciones_context(request):
    """
    Genera una lista de notificaciones relacionadas con el inventario.
    - Productos con stock bajo (< 20)
    - Productos inactivos
    - Productos nuevos en los últimos 2 días
    """
    notificaciones = []

    # Productos con bajo stock
    productos_bajo_stock = Producto.objects.filter(cantidad__lt=20, activo=True)
    for prod in productos_bajo_stock:
        notificaciones.append(f"⚠️ Stock bajo: {prod.nombre} ({prod.cantidad} unidades)")

    # Productos inactivos
    productos_inactivos = Producto.objects.filter(activo=False)
    for prod in productos_inactivos:
        notificaciones.append(f"❌ Producto inactivo: {prod.nombre}")

    # Productos nuevos en los últimos 2 días
    hace_2_dias = timezone.now() - timedelta(days=2)
    productos_nuevos = Producto.objects.filter(fecha_ingreso__gte=hace_2_dias)
    for prod in productos_nuevos:
        notificaciones.append(f"🆕 Producto agregado: {prod.nombre}")

    # Mostrar las notificaciones más recientes primero
    notificaciones.reverse()

    return {"notificaciones": notificaciones}


def carrito_count(request):
    """
    Retorna la cantidad total de ítems en el carrito del usuario autenticado.
    """
    if request.user.is_authenticated:
        carrito = Carrito.objects.filter(usuario=request.user, comprado=False).first()
        if carrito:
            total_items = sum(item.cantidad for item in carrito.items.all())
            return {'carrito_count': total_items}
    return {'carrito_count': 0}
