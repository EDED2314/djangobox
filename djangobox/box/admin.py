from django.contrib import admin

from .models import Location, Box, Item, ItemPortion, Unit, User, Loan
from import_export.admin import ExportActionMixin


class LocationAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ("name", "address", "postcode", "roomcode")


class BoxAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
        "location",
        "box",
    )
    list_filter = ["location"]
    search_fields = ["name"]


class ItemAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "sku",
        "mpn",
        "upc",
        "unit",
    )
    search_fields = (
        "name",
        "description",
        "sku",
        "mpn",
        "upc",
    )


class ItemPortionAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = (
        "item",
        "slug",
        "qty",
        "box",
    )
    search_fields = ("item__name", "slug", "box__name")


class LoanAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = (
        "item",
        "user",
        "qty",
        "qty_returned",
        "timestamp_borrow",
        "timestamp_return",
        "status",
    )
    list_filter = ("status", "user", "item")


admin.site.register(Location, LocationAdmin)
admin.site.register(Box, BoxAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(ItemPortion, ItemPortionAdmin)
admin.site.register(Loan, LoanAdmin)

admin.site.register(User)
admin.site.register(Unit)
