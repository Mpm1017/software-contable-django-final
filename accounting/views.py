from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Q
from .models import Transaction, Account, Category
from .forms import TransactionForm, AccountForm, CategoryForm


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
    total_income = transactions.filter(transaction_type='INCOME').aggregate(total=Sum('amount'))['total'] or 0
    total_expense = transactions.filter(transaction_type='EXPENSE').aggregate(total=Sum('amount'))['total'] or 0
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
    
    return render(request, 'accounting/transaction_list.html', context)


@login_required
def transaction_create(request):
    """
    Vista para crear una nueva transacción.
    """
    if request.method == 'POST':
        form = TransactionForm(request.POST, user=request.user)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            messages.success(request, '¡Transacción creada exitosamente!')
            return redirect('transaction_list')
    else:
        form = TransactionForm(user=request.user)
    
    context = {
        'form': form,
        'title': 'Nueva Transacción',
        'button_text': 'Crear Transacción'
    }
    
    return render(request, 'accounting/transaction_form.html', context)


@login_required
def transaction_update(request, pk):
    """
    Vista para editar una transacción existente.
    """
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Transacción actualizada exitosamente!')
            return redirect('transaction_list')
    else:
        form = TransactionForm(instance=transaction, user=request.user)
    
    context = {
        'form': form,
        'title': 'Editar Transacción',
        'button_text': 'Actualizar Transacción',
        'transaction': transaction
    }
    
    return render(request, 'accounting/transaction_form.html', context)


@login_required
def transaction_delete(request, pk):
    """
    Vista para eliminar una transacción.
    """
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    
    if request.method == 'POST':
        transaction.delete()
        messages.success(request, '¡Transacción eliminada exitosamente!')
        return redirect('transaction_list')
    
    context = {
        'transaction': transaction
    }
    
    return render(request, 'accounting/transaction_confirm_delete.html', context)


@login_required
def account_list(request):
    """
    Vista para listar todas las cuentas del usuario.
    """
    accounts = Account.objects.filter(user=request.user)
    
    context = {
        'accounts': accounts
    }
    
    return render(request, 'accounting/account_list.html', context)


@login_required
def account_create(request):
    """
    Vista para crear una nueva cuenta.
    """
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            messages.success(request, '¡Cuenta creada exitosamente!')
            return redirect('account_list')
    else:
        form = AccountForm()
    
    context = {
        'form': form,
        'title': 'Nueva Cuenta',
        'button_text': 'Crear Cuenta'
    }
    
    return render(request, 'accounting/account_form.html', context)


@login_required
def category_list(request):
    """
    Vista para listar todas las categorías del usuario.
    """
    categories = Category.objects.filter(user=request.user)
    
    context = {
        'categories': categories
    }
    
    return render(request, 'accounting/category_list.html', context)


@login_required
def category_create(request):
    """
    Vista para crear una nueva categoría.
    """
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            messages.success(request, '¡Categoría creada exitosamente!')
            return redirect('category_list')
    else:
        form = CategoryForm()
    
    context = {
        'form': form,
        'title': 'Nueva Categoría',
        'button_text': 'Crear Categoría'
    }
    
    return render(request, 'accounting/category_form.html', context)
