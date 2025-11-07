from django.urls import path
from . import views

urlpatterns = [
    # URLs de Transacciones
    path('transactions/', views.transaction_list, name='transaction_list'),
    path('transactions/create/', views.transaction_create, name='transaction_create'),
    path('transactions/<int:pk>/edit/', views.transaction_update, name='transaction_update'),
    path('transactions/<int:pk>/delete/', views.transaction_delete, name='transaction_delete'),
    
    # URLs de Cuentas
    path('accounts/', views.account_list, name='account_list'),
    path('accounts/create/', views.account_create, name='account_create'),
    
    # URLs de Categorías
    path('categories/', views.category_list, name='category_list'),
    path('categories/create/', views.category_create, name='category_create'),
    
    # URLs Administrativas
    path('admin/plan-cuentas/', views.admin_plan_cuentas, name='admin_plan_cuentas'),
    path('admin/asientos/', views.admin_asientos_contables, name='admin_asientos'),
    path('admin/reportes/', views.admin_reportes_financieros, name='admin_reportes'),
    path('admin/auditoria/', views.admin_auditoria, name='admin_auditoria'),
]
