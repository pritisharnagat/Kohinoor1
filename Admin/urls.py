from django.contrib import admin
from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
 
urlpatterns = [
    path('bootstrap/',bootstrap,name="bootstrap"),
    path('admin_add_product/',admin_add_product,name="admin_add_product"),
    path('add_blogs/',add_blogs,name="add_blogs"),
    path('view_blogs/',view_blogs,name="view_blogs"),
    path('blog_details/<int:id>/',blog_details,name="blog_details"),
    path('edit_blog/<int:id>/',edit_blog,name="edit_blog"),
    path('delete_blog/<int:id>/',delete_blog,name="delete_blog"),
    
    
    path('seller_register_list/',seller_register_list,name="seller_register_list"),
    path('seller_profile_view/<int:id>/',seller_profile_view,name="seller_profile_view"),
    path('seller_approved_list/',seller_approved_list,name="seller_approved_list"),
    path('seller_reject_list/',seller_reject_list,name="seller_reject_list"),
    
    path('approve_seller_product/',approve_seller_product,name="approve_seller_product"),
    path('admin_approve_product/<int:id>/', admin_approve_product, name='admin_approve_product'),
    path('admin_reject_product/<int:id>/', admin_reject_product, name='admin_reject_product'),
    path('approved_product/', approved_product, name='approved_product'),
    path('rejected_product/', rejected_product, name='rejected_product'),
    path('product_details/<int:id>/', product_details, name='product_details'),

    path('sellers_details/', sellers_details, name='sellers_details'),
    path('view-products/<int:user_id>/', view_products, name='view_products'),

    path('query_list/', query_list, name='query_list'),
    path('customer_queries/<int:id>/', customer_queries, name='customer_queries'),

    path('admin_all_products/', admin_all_products, name='admin_all_products'),

    # path('upload_product_image/', upload_product_image, name='upload_product_image'),

    
    path('view_invoice_no/',view_invoice_no, name='view_invoice_no'),

    

    path('preview/<int:product_id>/',preview, name='product_preview'),
    path('edit_admin_import/<int:id>/', edit_admin_import, name='edit_admin_import'),
    path('delete_admin_product/<str:prod_id>/', delete_admin_product, name='delete_admin_product'),
    # path('all_orders/',all_orders,name='all_orders'),

    path('order_status/', order_status, name='order_status'),
    path('view_order/<int:id>/', view_order, name='view_order'),
    path('update_status/', update_status, name='update_status'),

    path('all_orders/',all_orders,name='all_orders'),
    path('all_cancel_orders/',all_cancel_orders,name='all_cancel_orders'),
    path('show_return_orders/',show_return_orders,name='show_return_orders'),

    path('admin_availability_report/', admin_availability_report, name='admin_availability_report'),

    path('manage_commissions/', manage_commissions, name='manage_commissions'),
    path('approve_commission/<int:commission_id>/',approve_commission, name='approve_commission'),
    path('reject_commission/<int:commission_id>/',reject_commission, name='reject_commission'),
    path('move_to_pending/<int:commission_id>/', move_to_pending, name='move_to_pending'),
    path('approve/',approve_commissions, name='approve_commissions'),
    path('reject/',reject_commissions, name='reject_commissions'),

    path('excel_export_view/',excel_export_view,name='excel_export_view'),
    
    path('admin_payments/',admin_payments,name='admin_payments'),

    path('admin_dashboard/',admin_dashboard,name='admin_dashboard'),

    path('add_customize_design/',add_customize_design,name="add_customize_design"),

    path('all_customer_info/',all_customer_info,name="all_customer_info"),
    path('view-custproducts/<int:id>/', view_customerproducts, name='customer_products'),
    
    path("email-setting/", email_setting, name="email-setting"),

    path('aboutus/',aboutus,name="aboutus"),
    path('about_vr/', about_vr, name='about_vr'),

    path('faqs/', faq_questions, name='faqs'),
    path('display_faqs/', display_faqs, name='display_faqs'),

    path('add_events/',add_events,name="add_events"),
    path('view_events/',view_events,name="view_events"),
    path('edit_event/<int:id>/',edit_event,name="edit_event"),
    path('delete_event/<int:id>/',delete_event,name="delete_event"),
    
    path('inventory_listing/', inventory_listing, name='inventory_listing'),
    path('inventory_report/',inventory_report,name='inventory_report'),

    path('add_product/',add_product,name='add_product'),

    path('payment_setting/',payment_setting, name='payment_setting'),
    path('collections_thought/',collections_thought, name='collections_thought'),
    path('edit_collections_thought/',edit_collections_thought, name='edit_collections_thought'),
    path('edit_collections/<int:id>/',edit_collections, name='edit_collections'),
    path('delete_collections/<int:id>/', delete_collections, name='delete_collections'),

    path('admin_all_products_update/', admin_all_products_update, name='admin_all_products_update'),
    path('edit_product_details/<int:id>/', edit_product_details, name='edit_product_details'),



]
