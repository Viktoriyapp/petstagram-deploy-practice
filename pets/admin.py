from django.contrib import admin
from unfold.admin import ModelAdmin

from pets.models import Pet


# Register your models here.

@admin.register(Pet)
class PetAdmin(ModelAdmin):
    list_display = ['id','name', 'slug']