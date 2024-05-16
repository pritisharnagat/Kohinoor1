from django.urls import path, include,re_path
from .views import *

urlpatterns = [
    path("",home,name="home"),
    path("navbar/",navbar,name="navbar"),
    path('subscribe-newsletter/', subscribe_newsletter, name='subscribe_newsletter'),


    path("customer_register/",cust_registeration,name="cust_registeration"),
    path("customer_login/",cust_login,name="customer_login"),
    path("customer_after_login/",customer_after_login,name="customer_after_login"),
    path("seller_registeration/",seller_registeration,name="seller_registeration"),
    path("seller_login/",seller_login,name="seller_login"),
    path("seller_dashboard/",seller_dashboard,name="seller_dashboard"),
    path("admin_login/",admin_login,name="admin_login"),
    path("admin_dashboard/",admin_dashboard,name="admin_dashboard"),
    path('password_reset/', password_reset, name='password_reset'),
    path('password_change/', password_change, name='password_change'),
    path('customer_profile/', customer_profile,name="customer_profile"),   
    path('change_password/',change_password,name="change_password"),
    path('seller_profile/', seller_profile,name="seller_profile"),
    path('customer_logout/', customer_logout,name="customer_logout"),
    path('seller_logout/', seller_logout,name="seller_logout"),
    path('admin_logout/', admin_logout,name="admin_logout"),

    path('contact_us/', contact_us,name="contact_us"),
    path('privacy_policy/', privacy_policy,name="privacy_policy"),
    path('refund_&_return/', refund_and_return,name="refund_and_return"),
    path('terms_&_condition/', terms_and_condition,name="terms_and_condition"),
    path('shopping_faqs/', shopping_faqs,name="shopping_faqs"),

    path("cust_blog_login/",cust_blog_login,name="cust_blog_login"),
    path('blog_bhagatsingh/<str:title>/', blog_bhagatsingh,name="blog_bhagatsingh"),
    
    path('admin_profile/', admin_profile,name="admin_profile"),

    path('store_settings/', store_settings,name="store_settings"),
    path('customer_before_login/<str:prod_id>/', customer_before_login,name="customer_before_login"),
    
    path('customer_profile_checkout/', customer_profile_checkout,name="customer_profile_checkout"),

    


    # re_path(r'^(?!.*\.(?:jpg|png|gif|jpeg)$).*$', pages, name='pages'),
]


