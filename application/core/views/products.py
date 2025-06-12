from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from application.core.models import Producto
from application.core.forms.products_form import ProductoForm

class ProductoListView(ListView):
    model = Producto
    template_name = 'core/products/product_list.html'
    context_object_name = 'productos'

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

def catalogo_view(request):
    productos = Producto.objects.filter(activo=True)  # Mostrar solo productos activos
    return render(request, 'core/products/catalog_list.html', {'productos': productos})