from django.http import JsonResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from application.core.models import Categoria, Marca
from application.core.forms.category_form import CategoriaForm

class CategoriaListView(ListView):
    model = Categoria
    template_name = 'core/category/category_list.html'
    context_object_name = 'categorias'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['marcas'] = Marca.objects.all()
        return context


    
class CategoriaCreateView(CreateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'core/category/category_form.html'
    success_url = reverse_lazy('core:category_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear'
        return context
    
    def form_invalid(self, form):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
        return super().form_invalid(form)
    
class CategoriaUpdateView(UpdateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'core/category/category_form.html'
    success_url = reverse_lazy('core:category_list')


class CategoriaDeleteView(DeleteView):
    model = Categoria
    template_name = 'core/category/category_delete.html'
    success_url = reverse_lazy('core:category_list')

