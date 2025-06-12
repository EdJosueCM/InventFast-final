from django.http import JsonResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from application.core.models import Marca
from application.core.forms.brand_form import MarcaForm

class MarcaListView(ListView):
    model = Marca
    template_name = 'core/brand/brand_list.html'
    context_object_name = 'marcas'
    
class MarcaCreateView(CreateView):
    model = Marca
    form_class = MarcaForm
    template_name = 'core/brand/brand_form.html'
    success_url = reverse_lazy('core:category_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear'
        return context
    
    def form_invalid(self, form):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
        return super().form_invalid(form)
    
class MarcaUpdateView(UpdateView):
    model = Marca
    form_class = MarcaForm
    template_name = 'core/brand/brand_form.html'
    success_url = reverse_lazy('core:category_list')

class MarcaDeleteView(DeleteView):
    model = Marca
    template_name = 'core/brand/brand_delete.html'
    success_url = reverse_lazy('core:category_list')
