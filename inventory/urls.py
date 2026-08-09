from django.urls import path
from . import views


urlpatterns = [
    path(
        '',
        views.urun_listesi,
        name='urun_listesi'
    ),

    path(
        'urun-ekle/',
        views.urun_ekle,
        name='urun_ekle'
    ),

    path(
        'stok-girisi/<int:product_id>/',
        views.stok_girisi,
        name='stok_girisi'
    ),

    path(
        'stok-cikisi/<int:product_id>/',
        views.stok_cikisi,
        name='stok_cikisi'
    ),

    path(
        'hareket-gecmisi/<int:product_id>/',
        views.hareket_gecmisi,
        name='hareket_gecmisi'
    ),

    path(
        'urun-sil/<int:product_id>/',
        views.urun_sil,
        name='urun_sil'
    ),

    path(
    'urun-duzenle/<int:product_id>/',
        views.urun_duzenle,
        name='urun_duzenle'
    ),

    path(
    'tum-hareketler/',
        views.tum_hareketler,
        name='tum_hareketler'
    ),



]

