from django import forms
from .models import Transaction, Account, Category


class TransactionForm(forms.ModelForm):
    """
    Formulario para crear y editar transacciones.
    """
    class Meta:
        model = Transaction
        fields = ['account', 'category', 'transaction_type', 'amount', 'description', 'notes', 'transaction_date']
        widgets = {
            'account': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'category': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'transaction_type': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0.01',
                'required': True
            }),
            'description': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Pago de alquiler',
                'required': True
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Notas adicionales (opcional)',
                'rows': 3
            }),
            'transaction_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True
            }),
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Filtramos las cuentas y categorías para mostrar solo las del usuario actual
        if self.user:
            self.fields['account'].queryset = Account.objects.filter(user=self.user, is_active=True)
            self.fields['category'].queryset = Category.objects.filter(user=self.user, is_active=True)
    
    def clean(self):
        cleaned_data = super().clean()
        transaction_type = cleaned_data.get('transaction_type')
        category = cleaned_data.get('category')
        
        # Validamos que el tipo de transacción coincida con el tipo de categoría
        if transaction_type and category:
            if transaction_type != category.category_type:
                raise forms.ValidationError(
                    f'El tipo de transacción debe coincidir con el tipo de categoría. '
                    f'La categoría "{category.name}" es de tipo "{category.get_category_type_display()}".'
                )
        
        return cleaned_data


class AccountForm(forms.ModelForm):
    """
    Formulario para crear y editar cuentas.
    """
    class Meta:
        model = Account
        fields = ['name', 'account_type', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Cuenta Bancolombia',
                'required': True
            }),
            'account_type': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Descripción de la cuenta (opcional)',
                'rows': 3
            }),
        }


class CategoryForm(forms.ModelForm):
    """
    Formulario para crear y editar categorías.
    """
    class Meta:
        model = Category
        fields = ['name', 'category_type', 'description', 'color']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Salario',
                'required': True
            }),
            'category_type': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Descripción de la categoría (opcional)',
                'rows': 3
            }),
            'color': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'color',
                'required': True
            }),
        }
