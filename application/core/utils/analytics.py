import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.ensemble import RandomForestRegressor, IsolationForest
from sklearn.preprocessing import StandardScaler
from application.core.models import Producto, Factura, CarritoItem
from django.db.models import Sum

# Función para predecir ventas futuras por producto
def predecir_ventas_proximomes():
    facturas = Factura.objects.all().values('id', 'fecha')
    items = CarritoItem.objects.all().values('carrito_id', 'producto_id', 'cantidad')
    df_facturas = pd.DataFrame(facturas)
    df_items = pd.DataFrame(items)

    if df_facturas.empty or df_items.empty:
        return []

    df = df_items.merge(df_facturas, left_on='carrito_id', right_on='id')
    df['fecha'] = pd.to_datetime(df['fecha'])
    df['año_mes'] = df['fecha'].dt.to_period('M')
    
    # Agrupamos por mes y producto
    ventas_mensuales = df.groupby(['producto_id', 'año_mes'])['cantidad'].sum().reset_index()
    ventas_mensuales['año_mes'] = ventas_mensuales['año_mes'].astype(str)

    predicciones = []

    for producto_id, data in ventas_mensuales.groupby('producto_id'):
        if len(data) < 3:
            continue  # No hay suficiente historial

        data = data.copy()
        data['mes_idx'] = range(len(data))
        X = data[['mes_idx']]
        y = data['cantidad']

        modelo = RandomForestRegressor()
        modelo.fit(X, y)

        proximo_mes_idx = [[len(data)]]
        pred = modelo.predict(proximo_mes_idx)[0]

        producto = Producto.objects.filter(id=producto_id).first()
        if producto:
            predicciones.append({'producto': producto, 'prediccion': int(pred)})

    return sorted(predicciones, key=lambda x: -x['prediccion'])[:5]  # Top 5

# Función para detectar productos con baja rotación
def detectar_outliers_baja_rotacion():
    productos = Producto.objects.all()
    if not productos:
        return []

    data = []
    for p in productos:
        ventas = CarritoItem.objects.filter(producto=p).aggregate(total=Sum('cantidad'))['total'] or 0
        dias_en_catalogo = (datetime.now().date() - p.fecha_ingreso).days if p.fecha_ingreso else 1
        if dias_en_catalogo == 0:
            dias_en_catalogo = 1
        # Métrica de rotación: ventas por día
        rotacion = ventas / dias_en_catalogo
        data.append({'producto': p, 'rotacion': rotacion})

    # Ordenamos por menor rotación (menos ventas por día)
    ordenados = sorted(data, key=lambda x: x['rotacion'])

    # Tomamos los 5 productos con peor rotación
    peores = [d['producto'] for d in ordenados[:5]]

    return peores


def recomendar_reposicion_productos():
    facturas = Factura.objects.all().values('id', 'fecha')
    items = CarritoItem.objects.all().values('carrito_id', 'producto_id', 'cantidad')
    df_facturas = pd.DataFrame(facturas)
    df_items = pd.DataFrame(items)

    if df_facturas.empty or df_items.empty:
        return []

    df = df_items.merge(df_facturas, left_on='carrito_id', right_on='id')
    df['fecha'] = pd.to_datetime(df['fecha'])
    df['año_mes'] = df['fecha'].dt.to_period('M')

    # Agrupar por mes y producto
    ventas_mensuales = df.groupby(['producto_id', 'año_mes'])['cantidad'].sum().reset_index()
    ventas_mensuales['año_mes'] = ventas_mensuales['año_mes'].astype(str)

    recomendaciones = []

    for producto_id, data in ventas_mensuales.groupby('producto_id'):
        if len(data) < 3:
            continue  # No hay historial suficiente

        data = data.copy()
        data['mes_idx'] = range(len(data))
        X = data[['mes_idx']]
        y = data['cantidad']

        modelo = RandomForestRegressor()
        modelo.fit(X, y)

        proximo_mes_idx = [[len(data)]]
        prediccion = modelo.predict(proximo_mes_idx)[0]

        producto = Producto.objects.filter(id=producto_id).first()
        if producto:
            faltante = int(round(prediccion)) - producto.cantidad
            if faltante > 0:
                recomendaciones.append({
                    'producto': producto,
                    'estimado': int(round(prediccion)),
                    'stock': producto.cantidad,
                    'reponer': faltante
                })

    return recomendaciones

