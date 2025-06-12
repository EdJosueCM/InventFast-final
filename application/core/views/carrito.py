from django.shortcuts import get_object_or_404, redirect, render
from application.core.models import Producto, Carrito, CarritoItem, Factura, FacturaDetalle
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django.contrib import messages
from django.views.decorators.http import require_POST

@login_required
def view_cart(request):
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user, comprado=False)
    items = carrito.items.select_related('producto')
    total = sum(item.subtotal() for item in items)

    return render(request, 'core/checkout/view_cart.html', {
        'carrito': carrito,
        'items': items,
        'total': total
    })



@login_required
def add_to_cart(request, producto_id):
    if request.method == 'POST':
        cantidad = int(request.POST.get('cantidad', 1))
        producto = get_object_or_404(Producto, pk=producto_id)

        carrito, _ = Carrito.objects.get_or_create(usuario=request.user, comprado=False)
        item, creado = CarritoItem.objects.get_or_create(carrito=carrito, producto=producto)
        if creado:
            item.cantidad = cantidad  # Es nuevo, así que usamos directamente la cantidad indicada
        else:
            item.cantidad += cantidad  # Ya existía, sumamos la nueva cantidad

        item.save()

        messages.success(request, f"{producto.nombre} agregado al carrito.")
        return redirect('core:catalog_list')

@require_POST
@login_required
def update_cart(request, item_id):
    item = get_object_or_404(CarritoItem, pk=item_id, carrito__usuario=request.user, carrito__comprado=False)
    nueva_cantidad = int(request.POST.get('cantidad', item.cantidad))

    if nueva_cantidad > 0:
        item.cantidad = nueva_cantidad
        item.save()
        messages.success(request, f"Cantidad de {item.producto.nombre} actualizada.")
    else:
        item.delete()
        messages.info(request, f"{item.producto.nombre} fue eliminado del carrito.")

    return redirect('core:view_cart')

@login_required
def delete_item(request, item_id):
    item = get_object_or_404(CarritoItem, pk=item_id, carrito__usuario=request.user, carrito__comprado=False)

    if request.method == 'POST':
        item.delete()
        messages.success(request, "Producto eliminado del carrito.")
    return redirect('core:view_cart')  # Asegúrate que esta URL exista


@login_required
def checkout(request):
    carrito = Carrito.objects.filter(usuario=request.user, comprado=False).first()

    if not carrito or not carrito.items.exists():
        messages.error(request, "Tu carrito está vacío.")
        return redirect('ver_carrito')

    total = 0
    for item in carrito.items.all():
        if item.cantidad > item.producto.cantidad:
            messages.error(request, f"No hay suficiente stock de {item.producto.nombre}.")
            return redirect('ver_carrito')
        total += item.producto.precio * item.cantidad

    factura = Factura.objects.create(usuario=request.user, fecha=now(), total=total)

    for item in carrito.items.all():
        FacturaDetalle.objects.create(
            factura=factura,
            producto=item.producto,
            cantidad=item.cantidad,
            precio_unitario=item.producto.precio
        )
        item.producto.cantidad -= item.cantidad
        item.producto.save()

    carrito.comprado = True
    carrito.save()

    messages.success(request, "¡Compra realizada con éxito!")
    return redirect('core:invoice_detail', factura.id)
