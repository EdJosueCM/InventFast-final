import calendar
from datetime import timedelta
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from application.core.models import Factura, FacturaDetalle, Producto
from django.utils.timezone import now
from django.db.models.functions import TruncDate
from django.db.models import Sum
from django.utils.translation import gettext as _
from application.core.utils.analytics import *
from django.db.models import OuterRef, Subquery, IntegerField, Value
from django.db.models.functions import Coalesce

@login_required
def dashboard_view(request):
    # STOCK
    productos = Producto.objects.filter(activo=True).order_by('-cantidad')
    nombres = [p.nombre for p in productos]
    cantidades = [p.cantidad for p in productos]

    # OBTENER MES ACTUAL O SELECCIONADO
    hoy = now().date()
    mes = int(request.GET.get('mes', hoy.month))
    anio = hoy.year  

    # VENTAS FILTRADAS
    ventas = (
        Factura.objects
        .filter(fecha__year=anio, fecha__month=mes)
        .annotate(dia=TruncDate('fecha'))
        .values('dia')
        .annotate(total=Sum('total'))
        .order_by('dia')
    )

    dias = [v['dia'].strftime('%d %b') for v in ventas]
    totales = [float(v['total']) for v in ventas]
    meses = [(i, _(calendar.month_name[i])) for i in range(1, 13)]

    ventas_subquery = FacturaDetalle.objects.filter(producto=OuterRef('pk')) \
        .values('producto') \
        .annotate(total_vendido=Sum('cantidad')) \
        .values('total_vendido')

    productos_con_menos_ventas = Producto.objects.annotate(
        total_vendido=Coalesce(Subquery(ventas_subquery, output_field=IntegerField()), Value(0))
    ).order_by('total_vendido')[:5]

    productos_menos_nombre = [p.nombre for p in productos_con_menos_ventas]
    productos_menos_valor = [p.total_vendido for p in productos_con_menos_ventas]
    # Notificaciones
    notificaciones = []

    # Productos con bajo stock
    productos_bajo_stock = Producto.objects.filter(cantidad__lt=20, activo=True)
    for prod in productos_bajo_stock:
        notificaciones.append(f"⚠️ Stock bajo: {prod.nombre} ({prod.cantidad} unidades)")

    # Productos desactivados
    productos_inactivos = Producto.objects.filter(activo=False)
    for prod in productos_inactivos:
        notificaciones.append(f"❌ Producto inactivo: {prod.nombre}")

    ayer = now() - timedelta(hours=24)
    productos_nuevos = Producto.objects.filter(fecha_ingreso__gte=ayer, activo=True)
    for prod in productos_nuevos:
        notificaciones.append(f"🆕 Producto agregado: {prod.nombre}")

    predicciones = predecir_ventas_proximomes()
    productos_outliers = detectar_outliers_baja_rotacion()
    recomendaciones = recomendar_reposicion_productos()
    notificaciones.reverse()


    context = {
        'nombres': nombres,
        'cantidades': cantidades,
        'dias': dias,
        'totales': totales,
        'mes_actual': mes,
        'meses': meses,
        'menos_nombres': productos_menos_nombre,
        'menos_cantidades': productos_menos_valor,
        'notificaciones': notificaciones,
        'predicciones': predicciones,
        'productos_outliers': productos_outliers,
        'recomendaciones': recomendaciones,
    }
    

    return render(request, 'core/dashboard.html', context)
