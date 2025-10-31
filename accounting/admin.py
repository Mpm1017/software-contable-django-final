from django.contrib import admin
from .models import Account, Category, Transaction


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    """
    Configuración del panel de administración para Cuentas.
    """
    list_display = ['name', 'account_type', 'balance', 'user', 'is_active', 'created_at']
    list_filter = ['account_type', 'is_active', 'created_at']
    search_fields = ['name', 'description', 'user__username']
    readonly_fields = ['created_at', 'updated_at', 'balance']
    list_per_page = 20
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('user', 'name', 'account_type', 'description')
        }),
        ('Saldo', {
            'fields': ('balance',)
        }),
        ('Estado', {
            'fields': ('is_active',)
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Configuración del panel de administración para Categorías.
    """
    list_display = ['name', 'category_type', 'user', 'color', 'is_active', 'created_at']
    list_filter = ['category_type', 'is_active', 'created_at']
    search_fields = ['name', 'description', 'user__username']
    readonly_fields = ['created_at']
    list_per_page = 20
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('user', 'name', 'category_type', 'description')
        }),
        ('Personalización', {
            'fields': ('color',)
        }),
        ('Estado', {
            'fields': ('is_active',)
        }),
        ('Fechas', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    """
    Configuración del panel de administración para Transacciones.
    """
    list_display = ['description', 'transaction_type', 'amount', 'account', 'category', 'transaction_date', 'user']
    list_filter = ['transaction_type', 'transaction_date', 'category', 'account']
    search_fields = ['description', 'notes', 'user__username']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'transaction_date'
    list_per_page = 20
    
    fieldsets = (
        ('Información de la Transacción', {
            'fields': ('user', 'account', 'category', 'transaction_type')
        }),
        ('Detalles Financieros', {
            'fields': ('amount', 'transaction_date', 'description', 'notes')
        }),
        ('Fechas de Registro', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        """
        Aseguramos que el tipo de transacción coincida con el tipo de categoría.
        """
        if obj.category.category_type != obj.transaction_type:
            from django.contrib import messages
            messages.error(
                request,
                'El tipo de transacción debe coincidir con el tipo de categoría.'
            )
            return
        super().save_model(request, obj, form, change)
