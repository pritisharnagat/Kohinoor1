from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(product_seller)
admin.site.register(Commission)