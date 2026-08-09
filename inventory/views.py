from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import models
from django.contrib.auth.decorators import login_required

from .models import Product, StockMovement
from .forms import ProductForm, StockMovementForm

@login_required
def urun_listesi(request):
    arama = request.GET.get('arama', '')

    products = Product.objects.all().order_by('name')

    if arama:
        products = products.filter(name__icontains=arama)

    toplam_urun = Product.objects.count()

    dusuk_stok = Product.objects.filter(
        quantity__lte=models.F('minimum_stock')
    ).count()



    return render(
        request,
        'inventory/urun_listesi.html',
        {
            'products': products,
            'arama': arama,
            'toplam_urun': toplam_urun,
            'dusuk_stok': dusuk_stok,

        }
    )

@login_required
def urun_ekle(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)

        if form.is_valid():
            product = form.save(commit=False)

            product.quantity = 0
            product.save()

            messages.success(
                request,
                f'{product.name} ürünü oluşturuldu.'
            )

            return redirect('urun_listesi')

    else:
        form = ProductForm()

    return render(
        request,
        'inventory/urun_ekle.html',
        {
            'form': form
        }
    )
@login_required
def stok_girisi(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = StockMovementForm(request.POST)

        if form.is_valid():
            movement = form.save(commit=False)

            movement.product = product
            movement.movement_type = 'GIRIS'
            movement.save()

            product.quantity += movement.quantity
            product.save()

            messages.success(
                request,
                f'{product.name} için stok girişi yapıldı.'
            )

            return redirect('urun_listesi')

    else:
        form = StockMovementForm()

    return render(
        request,
        'inventory/stok_hareketi.html',
        {
            'form': form,
            'product': product,
            'islem': 'Stok Girişi',
        }
    )

@login_required
def stok_cikisi(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = StockMovementForm(request.POST)

        if form.is_valid():
            movement = form.save(commit=False)

            if movement.quantity > product.quantity:
                form.add_error(
                    'quantity',
                    'Çıkış miktarı mevcut stoktan fazla olamaz.'
                )

            else:
                movement.product = product
                movement.movement_type = 'CIKIS'
                movement.save()

                product.quantity -= movement.quantity
                product.save()

                messages.success(
                    request,
                    f'{product.name} için stok çıkışı yapıldı.'
                )

                return redirect('urun_listesi')

    else:
        form = StockMovementForm()

    return render(
        request,
        'inventory/stok_hareketi.html',
        {
            'form': form,
            'product': product,
            'islem': 'Stok Çıkışı',
        }
    )

@login_required
def hareket_gecmisi(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    movements = product.movements.all().order_by('-created_at')

    return render(
        request,
        'inventory/hareket_gecmisi.html',
        {
            'product': product,
            'movements': movements,
        }
    )

@login_required
def urun_sil(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        product.delete()

    return redirect('urun_listesi')

@login_required
def urun_duzenle(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)

        if form.is_valid():
            form.save()
            return redirect('urun_listesi')

    else:
        form = ProductForm(instance=product)

    return render(
        request,
        'inventory/urun_duzenle.html',
        {
            'form': form,
            'product': product,
        }
    )
@login_required
def tum_hareketler(request):
    movements = StockMovement.objects.select_related(
        'product'
    ).order_by('-created_at')

    return render(
        request,
        'inventory/tum_hareketler.html',
        {
            'movements': movements
        }
    )