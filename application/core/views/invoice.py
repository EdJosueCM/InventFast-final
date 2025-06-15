import json
from io import BytesIO
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from django.db.models import Sum, Value
from django.db.models.functions import Concat, ExtractMonth
from django.utils import timezone
from django.template.loader import render_to_string
from django.http import HttpResponse
from weasyprint import HTML

from application.core.models import Factura, FacturaDetalle


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


# Reporte en pantalla: Top 10 productos + Gráfico de ganancias

def reporte_productos_mas_vendidos(request):
    mes = request.GET.get('mes')
    if mes:
        try:
            mes = int(mes)
        except ValueError:
            mes = timezone.now().month
    else:
        mes = timezone.now().month

    anio = timezone.now().year

    productos_vendidos = (
        FacturaDetalle.objects
        .filter(factura__fecha__month=mes, factura__fecha__year=anio)
        .annotate(nombre_marca=Concat('producto__nombre', Value(' - '), 'producto__marca__nombre'))
        .values('nombre_marca')
        .annotate(total=Sum('cantidad'))
        .order_by('-total')[:10]
    )

    nombres = [p['nombre_marca'] for p in productos_vendidos]
    cantidades = [p['total'] for p in productos_vendidos]

    ganancias_qs = (
        Factura.objects
        .filter(fecha__year=anio)
        .annotate(mes=ExtractMonth('fecha'))
        .values('mes')
        .annotate(total=Sum('total'))
    )

    meses = [
        (1, "Enero"), (2, "Febrero"), (3, "Marzo"), (4, "Abril"), (5, "Mayo"),
        (6, "Junio"), (7, "Julio"), (8, "Agosto"), (9, "Septiembre"),
        (10, "Octubre"), (11, "Noviembre"), (12, "Diciembre"),
    ]
    labels = [nombre for _, nombre in meses]
    valores = [0] * 12

    for g in ganancias_qs:
        idx = g['mes'] - 1
        valores[idx] = float(g['total'])

    nombre_mes = dict(meses).get(mes, "")

    context = {
        'nombres_json': json.dumps(nombres),
        'cantidades_json': json.dumps(cantidades),
        'labels_json': json.dumps(labels),
        'valores_json': json.dumps(valores),
        'fecha_actual': timezone.now(),
        'mes': mes,
        'meses': meses,
        'nombre_mes': nombre_mes,
        'anio': anio,
    }
    return render(request, 'core/reports/mas_vendidos.html', context)


def reporte_mas_vendidos_pdf(request):
    if request.method == 'POST':
        mes = request.POST.get('mes') or request.GET.get('mes')
        if mes:
            try:
                mes = int(mes)
            except ValueError:
                mes = timezone.now().month
        else:
            mes = timezone.now().month

        anio = timezone.now().year

        productos_vendidos = (
            FacturaDetalle.objects
            .filter(factura__fecha__month=mes, factura__fecha__year=anio)
            .values('producto__nombre', 'producto__marca__nombre')
            .annotate(total=Sum('cantidad'))
            .order_by('-total')[:10]
        )

        meses = [
            (1, "Enero"), (2, "Febrero"), (3, "Marzo"), (4, "Abril"), (5, "Mayo"),
            (6, "Junio"), (7, "Julio"), (8, "Agosto"), (9, "Septiembre"),
            (10, "Octubre"), (11, "Noviembre"), (12, "Diciembre"),
        ]
        nombre_mes = dict(meses).get(mes, "")

        chart_image = request.POST.get('chart_image')

        html_string = render_to_string('core/reports/mas_vendidos_pdf.html', {
            'productos': productos_vendidos,
            'chart_image': chart_image,
            'nombre_mes': nombre_mes,
            'anio': anio,
        })

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="reporte_mas_vendidos.pdf"'

        pdf_file = BytesIO()
        HTML(string=html_string).write_pdf(pdf_file)
        pdf_file.seek(0)
        response.write(pdf_file.read())
        return response
    else:
        return HttpResponse("Método no permitido", status=405)


def reporte_ganancias_pdf(request):
    if request.method == 'POST':
        anio = timezone.now().year

        ganancias_qs = (
            Factura.objects
            .filter(fecha__year=anio)
            .annotate(mes=ExtractMonth('fecha'))
            .values('mes')
            .annotate(total=Sum('total'))
        )

        meses = [
            "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ]

        data = [{"mes": m, "total": 0} for m in meses]

        for g in ganancias_qs:
            idx = g['mes'] - 1
            data[idx]['total'] = float(g['total'])

        chart_image = request.POST.get('chart_image')

        html_string = render_to_string('core/reports/ganancias_pdf.html', {
            'ganancias': data,
            'chart_image': chart_image,
            'anio': anio,
        })

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="reporte_ganancias.pdf"'

        pdf_file = BytesIO()
        HTML(string=html_string).write_pdf(pdf_file)
        pdf_file.seek(0)
        response.write(pdf_file.read())
        return response
    else:
        return HttpResponse("Método no permitido", status=405)


def reporte_ganancias_mensuales(request):
    anio = timezone.now().year

    ganancias_qs = (
        Factura.objects
        .filter(fecha__year=anio)
        .annotate(mes=ExtractMonth('fecha'))
        .values('mes')
        .annotate(total=Sum('total'))
    )

    meses = [
        "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
    ]

    labels = meses[:]
    valores = [0] * 12

    for g in ganancias_qs:
        idx = g['mes'] - 1
        valores[idx] = float(g['total'])

    context = {
        'labels_json': json.dumps(labels),
        'valores_json': json.dumps(valores),
        'anio': anio,
    }
    return render(request, 'core/reports/ganancias_mensuales.html', context)
