from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from inventfast import settings

# Vistas organizadas y consistentes
from application.core import views
from application.core.views.home import inicio
from application.core.views.user import profile_view, profile_update_view, UserListView
from application.core.views.dashboard import dashboard_view
from application.core.views.products import (
    ProductoListView,
    ProductoCreateView,
    ProductoUpdateView,
    ProductoDeleteView,
    catalogo_view,
)
from application.core.views.category import (
    CategoriaListView,
    CategoriaCreateView,
    CategoriaUpdateView,
    CategoriaDeleteView,
)
from application.core.views.brand import (
    MarcaListView,
    MarcaCreateView,
    MarcaUpdateView,
    MarcaDeleteView,
)
from application.core.views.carrito import (
    add_to_cart,
    add_to_cart_ajax,
    view_cart,
    update_cart,
    delete_item,
    checkout,
)
from application.core.views.invoice import (
    FacturaListView,
    FacturaDetailView,
    reporte_productos_mas_vendidos,
    reporte_mas_vendidos_pdf,
    reporte_ganancias_pdf,
    reporte_ganancias_mensuales,  # ✅ Importado correctamente
)
from application.core.views.graphics import grafico_stock_view
from application.security.views import auth

app_name = "core"

urlpatterns = [
    # ✅ Inicio y Autenticación
    path("inicio", inicio, name="inicio"),
    path("signup/", auth.signup, name="signup"),
    path("login/", auth.login_view, name="login"),
    path("logout/", auth.logout_view, name="logout"),

    # ✅ Perfil de usuario
    path("profile/", profile_view, name="profile"),
    path("profile_update", profile_update_view, name="profile_update"),

    # ✅ Dashboard
    path("dashboard/", dashboard_view, name="dashboard"),

    # ✅ Productos
    path("product_list/", ProductoListView.as_view(), name="product_list"),
    path("product_create/", ProductoCreateView.as_view(), name="product_create"),
    path("product_delete/<int:pk>/", ProductoDeleteView.as_view(), name="product_delete"),
    path("product_update/<int:pk>/", ProductoUpdateView.as_view(), name="product_update"),

    # ✅ Catálogo
    path("catalog_list/", catalogo_view, name="catalog_list"),

    # ✅ Categorías
    path("category_list/", CategoriaListView.as_view(), name="category_list"),
    path("category_create/", CategoriaCreateView.as_view(), name="category_create"),
    path("category_delete/<int:pk>/", CategoriaDeleteView.as_view(), name="category_delete"),
    path("category_update/<int:pk>/", CategoriaUpdateView.as_view(), name="category_update"),

    # ✅ Marcas
    path("brand_list", MarcaListView.as_view(), name="brand_list"),
    path("brand_create", MarcaCreateView.as_view(), name="brand_create"),
    path("brand_delete/<int:pk>/", MarcaDeleteView.as_view(), name="brand_delete"),
    path("brand_update/<int:pk>/", MarcaUpdateView.as_view(), name="brand_update"),

    # ✅ Usuarios
    path("users/", UserListView.as_view(), name="user_list"),

    # ✅ Carrito de compras
    path("add_to_cart/<int:producto_id>/", add_to_cart, name="add_to_cart"),
    path("view_cart/", view_cart, name="view_cart"),
    path("update_item/<int:item_id>/", update_cart, name="update_item"),
    path("delete_item/<int:item_id>/", delete_item, name="delete_item"),
    path("checkout/", checkout, name="checkout"),
    path("add_to_cart_ajax/", add_to_cart_ajax, name="add_to_cart_ajax"),


    # ✅ Facturas
    path("invoice_list/", FacturaListView.as_view(), name="invoice_list"),
    path("invoice_detail/<int:pk>/", FacturaDetailView.as_view(), name="invoice_detail"),

    # ✅ Gráfico de stock
    path("graphic_stock/", grafico_stock_view, name="graphic_stock"),

    # ✅ Reportes (productos y ganancias)
    path("reports/mas_vendidos/", reporte_productos_mas_vendidos, name="reporte_mas_vendidos"),
    path("reports/mas_vendidos/pdf/", reporte_mas_vendidos_pdf, name="reporte_mas_vendidos_pdf"),
    path("reports/ganancias_pdf/", reporte_ganancias_pdf, name="reporte_ganancias_pdf"),
    path("reports/ganancias/", reporte_ganancias_mensuales, name="reporte_ganancias_mensuales"),

    # ✅ Password Reset
    path(
        "reset_password/",
        auth_views.PasswordResetView.as_view(
            template_name="core/password_reset/reset_password.html",
            email_template_name="core/password_reset/password_reset_email.html",
            success_url=reverse_lazy("core:password_reset_done"),
        ),
        name="reset_password",
    ),
    path(
        "reset_password_send/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="core/password_reset/reset_password_done.html",
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="core/password_reset/password_reset_confirm.html",
            success_url=reverse_lazy("core:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset_password_complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="core/password_reset/password_reset_complete.html",
        ),
        name="password_reset_complete",
    ),
]

# ✅ Servir media en modo DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
