from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from application.core.models import Factura
from django.core.exceptions import PermissionDenied


class FacturaListView(LoginRequiredMixin, ListView):
    model = Factura
    template_name = 'core/invoices/invoice_list.html'
    context_object_name = 'facturas'

    def get_queryset(self):
        return Factura.objects.filter(usuario=self.request.user).order_by('-fecha')


class FacturaDetailView(LoginRequiredMixin, DetailView):
    model = Factura
    template_name = 'core/invoices/invoice_detail.html'
    context_object_name = 'factura'

    def get_object(self):
        factura = super().get_object()
        if factura.usuario != self.request.user:
            raise PermissionDenied()
        return factura
