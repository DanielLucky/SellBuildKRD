from django.contrib import admin
from .models import Sell
# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ("pk", "nameSell", "price", "author", "pub_date")
    search_fields = ("specifications",)
    list_filter = ("pub_date",)


admin.site.register(Sell, PostAdmin)
