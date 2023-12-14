from django.contrib import admin
from . models import category, product
# Register your models here.


class catadmin(admin.ModelAdmin):
    list_display = ['name','slug']
    prepopulated_fields={'slug':('name',)}
admin.site.register(category, catadmin)

class proadmin(admin.ModelAdmin):
    list_display = ['name','stock','price','desc','available', 'img']
    list_editable = ['stock','price','available', 'img']
    prepopulated_fields={'slug':('name',)}
admin.site.register(product, proadmin)