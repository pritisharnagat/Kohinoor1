"""
URL configuration for Vishwaratna project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static #new
from django.conf import settings
from login import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('Admin.urls')),
    path('',include('customer.urls')),
    path('',include('seller.urls')),
    path('',include('login.urls')),
    path('',views.home, name='home'),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('auth/', include('social_django.urls', namespace='social')),
    # path('login/', auth_views.LoginView.as_view(), name='login'),
    # path('oauth/', include('social_django.urls', namespace='social')),
    # path('auth/', include('social_django.urls', namespace='social')),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    # path('accounts/login/', LoginView.as_view(), name='login'),
    path('social-auth/', include('social_django.urls', namespace="social")),
    


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_URL)