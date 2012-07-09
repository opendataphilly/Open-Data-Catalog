from django.contrib import admin

from warehouse.models import Warehouse


#class WarehouseAdmin(admin.ModelAdmin):
#    list_display = ['group', 'bucket_name']
#    search_fields = ['bucket_name']
#    list_filter = ['bucket_name']


admin.site.register(Warehouse) #, WarehouseAdmin)

