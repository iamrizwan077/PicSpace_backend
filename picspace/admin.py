from django.contrib import admin
from .models import Gallery  # CustomUser
# Register your models here.


@admin.register(Gallery)
class GalleryModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'image_uuid', 'image_size', 'date']
