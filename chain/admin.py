from django.contrib import admin
from chain.models import ChainUser, cropImage, Product, Orders, OrderUpdate
from import_export.admin import ImportExportModelAdmin
# Register your models here.

class BrandAdmin(ImportExportModelAdmin):
    pass

admin.site.register(cropImage)
admin.site.register(ChainUser)
admin.site.register(Product, BrandAdmin)
admin.site.register(Orders, BrandAdmin)
admin.site.register(OrderUpdate)
