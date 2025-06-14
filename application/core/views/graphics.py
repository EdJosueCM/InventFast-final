from django.shortcuts import render
from application.core.models import Producto

def grafico_stock_view(request):
    productos = Producto.objects.filter(activo=True).order_by('-cantidad')
    nombres = [p.nombre for p in productos]
    cantidades = [p.cantidad for p in productos]

    context = {
        'nombres': nombres,
        'cantidades': cantidades
    }
    return render(request, 'core/dashboard/dashboard.html', context)
