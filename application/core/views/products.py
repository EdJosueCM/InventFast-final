from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from application.core.models import Producto, Categoria
from application.core.forms.products_form import ProductoForm
from django.core.paginator import Paginator
import unicodedata

# ✅ Función para normalizar texto: quita tildes y pasa a minúsculas
def normalizar(texto):
    if not texto:
        return ''
    return ''.join(
        c for c in unicodedata.normalize('NFKD', texto)
        if not unicodedata.combining(c)
    ).lower()

class ProductoListView(ListView):
    model = Producto
    template_name = 'core/products/product_list.html'
    context_object_name = 'productos'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q', '')

        if query:
            query_normalizada = normalizar(query)
            resultados = []

            for producto in queryset:
                nombre = normalizar(producto.nombre)
                categoria = normalizar(producto.categoria.nombre)
                marca = normalizar(producto.marca.nombre) if producto.marca else ''

                if query_normalizada in nombre or query_normalizada in categoria or query_normalizada in marca:
                    resultados.append(producto)

            return resultados

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context

class ProductoCreateView(CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'core/products/product_form.html'
    success_url = reverse_lazy('core:product_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear'
        return context

    def form_invalid(self, form):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
        return super().form_invalid(form)

class ProductoUpdateView(UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'core/products/product_form.html'
    success_url = reverse_lazy('core:product_list')

class ProductoDeleteView(DeleteView):
    model = Producto
    template_name = 'core/products/product_delete.html'
    success_url = reverse_lazy('core:product_list')

# ✅ Vista de catálogo con búsqueda IGNORANDO TILDES
def catalogo_view(request):
    query = request.GET.get("q", "").strip()
    categoria_id = request.GET.get("categoria")

    # Limpiar ID de categoría
    if categoria_id in [None, '', 'None']:
        categoria_id = None
    else:
        categoria_id = int(categoria_id)

    # Filtrar productos activos
    productos_qs = Producto.objects.filter(activo=True)
    productos = list(productos_qs)

    if query:
        query_normalizada = normalizar(query)
        productos = [
            p for p in productos
            if query_normalizada in normalizar(p.nombre)
        ]

    if categoria_id:
        productos = [p for p in productos if p.categoria_id == categoria_id]

    paginator = Paginator(productos, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, 'core/products/catalog_list.html', {
        'productos': page_obj,
        'query': query,
        'categoria_id': categoria_id,
        'categorias': Categoria.objects.all(),
        'is_paginated': page_obj.has_other_pages(),
        'page_obj': page_obj,
        # ❌ ya no incluimos carrito_count manualmente aquí
    })
