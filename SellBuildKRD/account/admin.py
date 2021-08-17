from django.contrib import admin
from django.apps import apps
from .models import ContactSend


# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ("pk", "imageSell", 'sellId',)


class PostAdminContact(admin.ModelAdmin):
    list_display = ("pk", "name_agent", 'theme', 'message')


Image = apps.get_model('Sell', 'Image')

admin.site.register(Image, PostAdmin)
admin.site.register(ContactSend, PostAdminContact)
