from django import forms
from .models import Product, StockMovement


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'unit', 'minimum_stock']

        labels = {
            'name': 'Ürün Adı',
            'category': 'Kategori',
            'unit': 'Birim',
            'minimum_stock': 'Minimum Stok',
        }


class StockMovementForm(forms.ModelForm):
    class Meta:
        model = StockMovement
        fields = ['quantity', 'description']

        labels = {
            'quantity': 'Miktar',
            'description': 'Açıklama',
        }

        widgets = {
            'quantity': forms.NumberInput(
                attrs={
                    'min': 1,
                    'placeholder': 'Miktar girin'
                }
            ),

            'description': forms.TextInput(
                attrs={
                    'placeholder': 'Örn. Davlumbaz üretimi'
                }
            ),
        }