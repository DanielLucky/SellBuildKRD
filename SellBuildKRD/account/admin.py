from django.contrib import admin
from django.apps import apps

# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ("pk", "imageSell", 'sellId', )


Image = apps.get_model('Sell', 'Image')

admin.site.register(Image, PostAdmin)