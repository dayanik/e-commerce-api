from django.contrib import admin

from . import models

class ProductAdmin(admin.ModelAdmin):
    fields = ["title", "description", "price"]
    list_display = ["title", "description", "price"]
    search_fields = ["title", "description"]


admin.site.register(models.Product, ProductAdmin)
