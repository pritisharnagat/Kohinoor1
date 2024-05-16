from django.contrib import admin
from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
 
urlpatterns = [
    path('seller_base/',seller_base,name="seller_base"),
    path('seller_add_product/', seller_add_product, name='seller_add_product'),
    path('admin_approved_products/', admin_approved_products, name='admin_approved_products'),
    path('seller_all_products/', seller_all_products, name='seller_all_products'),

    path('seller_commission_form/',seller_commission_form,name='seller_commission_form'),
    path('seller_view_invoice/',seller_view_invoice, name='seller_view_invoice'),

    path('update_product/<int:product_id>/',update_product, name='update_product'),
    path('delete_product/<int:product_id>/',delete_product, name='delete_product'),
    path('preview/<int:product_id>/', preview_product, name='preview_product'),

    path('seller_cancel_orders/',seller_cancel_orders,name='seller_cancel_orders'),
    path('seller_return_orders/',seller_return_orders,name='show_return_orders'),
    path('seller_all_orders/',seller_all_orders,name='seller_all_orders'),

    path('availability_report/',availability_report,name='availability_report'),

    path('seller_order_tracking/',seller_order_tracking,name='seller_order_tracking'),

    path('edit_seller_import/<int:id>/', edit_seller_import, name='edit_seller_import'),

    path('view_order_seller/<int:id>/', view_order_seller, name='view_order_seller'),


]