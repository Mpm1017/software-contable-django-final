from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Q
from django.contrib.auth.models import User
from django.contrib.admin.models import LogEntry
from .models import Transaction, Account, Category, AsientoContable, CuentaContable
from .forms import TransactionForm, AccountForm, CategoryForm

# ================================================
# CONSTANTES
# ================================================

# Tipos de transacción
TRANSACTION_TYPE_INCOME = 'INCOME'
TRANSACTION_TYPE_EXPENSE = 'EXPENSE'

# Mensajes
MSG_NO_PERMISOS = 'No tienes permisos para acceder a esta sección.'
MSG_TRANSACCION_CREADA = '¡Transacción creada exitosamente!'
MSG_TRANSACCION_ACTUALIZADA = '¡Transacción actualizada exitosamente!'
MSG_TRANSACCION_ELIMINADA = '¡Transacción eliminada exitosamente!'
MSG_CUENTA_CREADA = '¡Cuenta creada exitosamente!'
MSG_CATEGORIA_CREADA = '¡Categoría creada exitosamente!'

# Nombres de vistas/redirecciones
VIEW_TRANSACTION_LIST = 'transaction_list'
VIEW_ACCOUNT_LIST = 'account_list'
VIEW_CATEGORY_LIST = 'category_list'
VIEW_USER_DASHBOARD = 'user_dashboard'

# Templates
TEMPLATE_TRANSACTION_LIST = 'accounting/transaction_list.html'
TEMPLATE_TRANSACTION_FORM = 'accounting/transaction_form.html'
TEMPLATE_TRANSACTION_DELETE = 'accounting/transaction_confirm_delete.html'
TEMPLATE_ACCOUNT_LIST = 'accounting/account_list.html'
TEMPLATE_ACCOUNT_FORM = 'accounting/account_form.html'
TEMPLATE_CATEGORY_LIST = 'accounting/category_list.html'
TEMPLATE_CATEGORY_FORM = 'accounting/category_form.html'
TEMPLATE_ADMIN_PLAN_CUENTAS = 'accounting/admin_plan_cuentas.html'
TEMPLATE_ADMIN_ASIENTOS = 'accounting/admin_asientos.html'
TEMPLATE_ADMIN_REPORTES = 'accounting/admin_reportes.html'
TEMPLATE_ADMIN_AUDITORIA = 'accounting/admin_auditoria.html'

# Parámetros HTTP
HTTP_METHOD_POST = 'POST'


@login_required
def transaction_list(request):
    """
    Vista para listar todas las transacciones del usuario.
    """
    transactions = Transaction.objects.filter(user=request.user)
    
    # Filtros opcionales
    transaction_type = request.GET.get('type')
    account_id = request.GET.get('account')
    category_id = request.GET.get('category')
    
    if transaction_type:
        transactions = transactions.filter(transaction_type=transaction_type)
    if account_id:
        transactions = transactions.filter(account_id=account_id)
    if category_id:
        transactions = transactions.filter(category_id=category_id)
    
    # Estadísticas
    total_income = transactions.filter(transaction_type=TRANSACTION_TYPE_INCOME).aggregate(total=Sum('amount'))['total'] or 0
    total_expense = transactions.filter(transaction_type=TRANSACTION_TYPE_EXPENSE).aggregate(total=Sum('amount'))['total'] or 0
    balance = total_income - total_expense
    
    # Datos para los filtros
    accounts = Account.objects.filter(user=request.user, is_active=True)
    categories = Category.objects.filter(user=request.user, is_active=True)
    
    context = {
        'transactions': transactions,
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'accounts': accounts,
        'categories': categories,
    }
    
    return render(request, TEMPLATE_TRANSACTION_LIST, context)


@login_required
def transaction_create(request):
    """
    Vista para crear una nueva transacción.
    """
    if request.method == HTTP_METHOD_POST:
        form = TransactionForm(request.POST, user=request.user)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            messages.success(request, MSG_TRANSACCION_CREADA)
            return redirect(VIEW_TRANSACTION_LIST)
    else:
        form = TransactionForm(user=request.user)
    
    context = {
        'form': form,
        'title': 'Nueva Transacción',
        'button_text': 'Crear Transacción'
    }
    
    return render(request, TEMPLATE_TRANSACTION_FORM, context)


@login_required
def transaction_update(request, pk):
    """
    Vista para editar una transacción existente.
    """
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    
    if request.method == HTTP_METHOD_POST:
        form = TransactionForm(request.POST, instance=transaction, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, MSG_TRANSACCION_ACTUALIZADA)
            return redirect(VIEW_TRANSACTION_LIST)
    else:
        form = TransactionForm(instance=transaction, user=request.user)
    
    context = {
        'form': form,
        'title': 'Editar Transacción',
        'button_text': 'Actualizar Transacción',
        'transaction': transaction
    }
    
    return render(request, TEMPLATE_TRANSACTION_FORM, context)


@login_required
def transaction_delete(request, pk):
    """
    Vista para eliminar una transacción.
    """
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    
    if request.method == HTTP_METHOD_POST:
        transaction.delete()
        messages.success(request, MSG_TRANSACCION_ELIMINADA)
        return redirect(VIEW_TRANSACTION_LIST)
    
    context = {
        'transaction': transaction
    }
    
    return render(request, TEMPLATE_TRANSACTION_DELETE, context)


@login_required
def account_list(request):
    """
    Vista para listar todas las cuentas del usuario.
    """
    accounts = Account.objects.filter(user=request.user)
    
    context = {
        'accounts': accounts
    }
    
    return render(request, TEMPLATE_ACCOUNT_LIST, context)


@login_required
def account_create(request):
    """
    Vista para crear una nueva cuenta.
    """
    if request.method == HTTP_METHOD_POST:
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            messages.success(request, MSG_CUENTA_CREADA)
            return redirect(VIEW_ACCOUNT_LIST)
    else:
        form = AccountForm()
    
    context = {
        'form': form,
        'title': 'Nueva Cuenta',
        'button_text': 'Crear Cuenta'
    }
    
    return render(request, TEMPLATE_ACCOUNT_FORM, context)


@login_required
def category_list(request):
    """
    Vista para listar todas las categorías del usuario.
    """
    categories = Category.objects.filter(user=request.user)
    
    context = {
        'categories': categories
    }
    
    return render(request, TEMPLATE_CATEGORY_LIST, context)


@login_required
def category_create(request):
    """
    Vista para crear una nueva categoría.
    """
    if request.method == HTTP_METHOD_POST:
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            messages.success(request, MSG_CATEGORIA_CREADA)
            return redirect(VIEW_CATEGORY_LIST)
    else:
        form = CategoryForm()
    
    context = {
        'form': form,
        'title': 'Nueva Categoría',
        'button_text': 'Crear Categoría'
    }
    
    return render(request, TEMPLATE_CATEGORY_FORM, context)


# ================================================
# VISTAS ADMINISTRATIVAS
# ================================================

@login_required
def admin_plan_cuentas(request):
    """
    Vista para administradores: Plan de Cuentas completo del sistema.
    """
    # Verificar que sea administrador
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, MSG_NO_PERMISOS)
        return redirect(VIEW_USER_DASHBOARD)
    
    # Obtener todas las cuentas contables del sistema
    cuentas = CuentaContable.objects.all().order_by('codigo')
    
    # Estadísticas
    total_cuentas = cuentas.count()
    cuentas_activas = cuentas.filter(activa=True).count()
    
    context = {
        'cuentas': cuentas,
        'total_cuentas': total_cuentas,
        'cuentas_activas': cuentas_activas,
    }
    
    return render(request, TEMPLATE_ADMIN_PLAN_CUENTAS, context)


@login_required
def admin_asientos_contables(request):
    """
    Vista para administradores: Ver todos los asientos contables del sistema.
    """
    # Verificar que sea administrador
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, MSG_NO_PERMISOS)
        return redirect(VIEW_USER_DASHBOARD)
    
    # Obtener todos los asientos contables
    asientos = AsientoContable.objects.all().order_by('-fecha', '-numero')
    
    # Filtros opcionales
    usuario_id = request.GET.get('usuario')
    if usuario_id:
        asientos = asientos.filter(usuario_id=usuario_id)
    
    # Estadísticas
    total_asientos = asientos.count()
    usuarios = User.objects.filter(is_staff=False)
    
    context = {
        'asientos': asientos,
        'total_asientos': total_asientos,
        'usuarios': usuarios,
    }
    
    return render(request, TEMPLATE_ADMIN_ASIENTOS, context)


@login_required
def admin_reportes_financieros(request):
    """
    Vista para administradores: Reportes financieros globales del sistema.
    """
    # Verificar que sea administrador
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, MSG_NO_PERMISOS)
        return redirect(VIEW_USER_DASHBOARD)
    
    # Calcular totales globales
    total_ingresos = Transaction.objects.filter(transaction_type=TRANSACTION_TYPE_INCOME).aggregate(total=Sum('amount'))['total'] or 0
    total_gastos = Transaction.objects.filter(transaction_type=TRANSACTION_TYPE_EXPENSE).aggregate(total=Sum('amount'))['total'] or 0
    balance_general = total_ingresos - total_gastos
    
    # Transacciones por usuario
    usuarios_stats = []
    for user in User.objects.filter(is_staff=False):
        user_income = Transaction.objects.filter(user=user, transaction_type=TRANSACTION_TYPE_INCOME).aggregate(total=Sum('amount'))['total'] or 0
        user_expense = Transaction.objects.filter(user=user, transaction_type=TRANSACTION_TYPE_EXPENSE).aggregate(total=Sum('amount'))['total'] or 0
        usuarios_stats.append({
            'usuario': user.username,
            'ingresos': user_income,
            'gastos': user_expense,
            'balance': user_income - user_expense
        })
    
    context = {
        'total_ingresos': total_ingresos,
        'total_gastos': total_gastos,
        'balance_general': balance_general,
        'usuarios_stats': usuarios_stats,
    }
    
    return render(request, TEMPLATE_ADMIN_REPORTES, context)


@login_required
def admin_auditoria(request):
    """
    Vista para administradores: Auditoría y logs del sistema.
    """
    # Verificar que sea administrador
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, MSG_NO_PERMISOS)
        return redirect(VIEW_USER_DASHBOARD)
    
    # Obtener logs de Django Admin
    logs = LogEntry.objects.all().order_by('-action_time')[:100]
    
    # Estadísticas de actividad
    total_usuarios = User.objects.count()
    usuarios_activos = User.objects.filter(is_active=True).count()
    total_transacciones = Transaction.objects.count()
    
    context = {
        'logs': logs,
        'total_usuarios': total_usuarios,
        'usuarios_activos': usuarios_activos,
        'total_transacciones': total_transacciones,
    }
    
    return render(request, TEMPLATE_ADMIN_AUDITORIA, context)
