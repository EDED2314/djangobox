from django.contrib import admin

from .models import Location, Box, Item, ItemPortion, Unit, User
from import_export.admin import ExportActionMixin


class LocationAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ("name", "address", "postcode", "roomcode")


class BoxAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ("name", "location")


class ItemAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = list_display = (
        "name",
        "description",
        "sku",
        "mpn",
        "upc",
        "unit",
    )


class ItemPortionAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = list_display = (
        "item",
        "uuid",
        "qty",
        "box",
    )


admin.site.register(Location, LocationAdmin)
admin.site.register(Box, BoxAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(ItemPortion, ItemPortionAdmin)

admin.site.register(User)
admin.site.register(Unit)
