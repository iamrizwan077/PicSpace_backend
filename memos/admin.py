from django.contrib import admin
from .models import Gallery,CustomUser
# Register your models here.
@admin.register(Gallery)
class GalleryModelAdmin(admin.ModelAdmin):
  list_display=['id','name','image','date']

@admin.register(CustomUser)
class CustomModelAdmin(admin.ModelAdmin):
  list_display = ['id','username','email']

