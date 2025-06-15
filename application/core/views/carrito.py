from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils.timezone import now
from django.contrib import messages
from django.db.models import Sum

from application.core.models import (
    Producto,
    Carrito,
    CarritoItem,
    Factura,
    FacturaDetalle,
)


# 🛒 Ver carrito
@login_required
def view_cart(request):
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user, comprado=False)
    items = carrito.items.select_related("producto")
    total = sum(item.subtotal() for item in items)
    return render(
        request,
        "core/checkout/view_cart.html",
        {"carrito": carrito, "items": items, "total": total},
    )


# 🛒 Agregar producto al carrito (normal)
@login_required
def add_to_cart(request, producto_id):
    if request.method == "POST":
        cantidad = int(request.POST.get("cantidad", 1))
        producto = get_object_or_404(Producto, pk=producto_id)

        carrito, _ = Carrito.objects.get_or_create(usuario=request.user, comprado=False)
        item, creado = CarritoItem.objects.get_or_create(
            carrito=carrito, producto=producto
        )

        item.cantidad = item.cantidad + cantidad if not creado else cantidad
        item.save()

        messages.success(request, f"{producto.nombre} agregado al carrito.")
        return redirect("core:catalog_list")


# 🛒 Agregar producto al carrito vía AJAX (sin recargar)
@login_required
@require_POST
def add_to_cart_ajax(request):
    producto_id = request.POST.get("producto_id")
    cantidad = int(request.POST.get("cantidad", 1))
    producto = get_object_or_404(Producto, pk=producto_id)

    carrito, _ = Carrito.objects.get_or_create(usuario=request.user, comprado=False)
    item, creado = CarritoItem.objects.get_or_create(carrito=carrito, producto=producto)

    item.cantidad = item.cantidad + cantidad if not creado else cantidad
    item.save()

    # Calcular el total actualizado de productos en el carrito
    total_items = carrito.items.aggregate(total=Sum('cantidad'))['total'] or 0

    return JsonResponse({
        "ok": True,
        "mensaje": f"Has agregado {cantidad}x {producto.nombre} a tu carrito",
        "cantidad": item.cantidad,
        "producto": producto.nombre,
        "carrito_count": total_items,
    })


# 🔁 Actualizar cantidad de un ítem
@require_POST
@login_required
def update_cart(request, item_id):
    item = get_object_or_404(
        CarritoItem, pk=item_id, carrito__usuario=request.user, carrito__comprado=False
    )
    nueva_cantidad = int(request.POST.get("cantidad", item.cantidad))

    if nueva_cantidad > 0:
        item.cantidad = nueva_cantidad
        item.save()
        messages.success(request, f"Cantidad de {item.producto.nombre} actualizada.")
    else:
        item.delete()
        messages.info(request, f"{item.producto.nombre} fue eliminado del carrito.")

    return redirect("core:view_cart")


# ❌ Eliminar producto del carrito
@login_required
def delete_item(request, item_id):
    item = get_object_or_404(
        CarritoItem, pk=item_id, carrito__usuario=request.user, carrito__comprado=False
    )
    if request.method == "POST":
        item.delete()
        messages.success(request, "Producto eliminado del carrito.")
    return redirect("core:view_cart")


# ✅ Confirmar compra
@login_required
def checkout(request):
    carrito = Carrito.objects.filter(usuario=request.user, comprado=False).first()

    if not carrito or not carrito.items.exists():
        messages.error(request, "Tu carrito está vacío.")
        return redirect("core:view_cart")

    total = 0
    for item in carrito.items.all():
        if item.cantidad > item.producto.cantidad:
            messages.error(request, f"No hay suficiente stock de {item.producto.nombre}.")
            return redirect("core:view_cart")
        total += item.producto.precio * item.cantidad

    factura = Factura.objects.create(usuario=request.user, fecha=now(), total=total)

    for item in carrito.items.all():
        FacturaDetalle.objects.create(
            factura=factura,
            producto=item.producto,
            cantidad=item.cantidad,
            precio_unitario=item.producto.precio,
        )
        item.producto.cantidad -= item.cantidad
        item.producto.save()

    carrito.comprado = True
    carrito.save()

    messages.success(request, "¡Compra realizada con éxito!")
    return redirect("core:invoice_detail", factura.id)
