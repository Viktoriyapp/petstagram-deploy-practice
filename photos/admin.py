from django.contrib import admin
from unfold.admin import ModelAdmin

from photos.models import Photo


# Register your models here.

@admin.register(Photo)
class PhotoAdmin(ModelAdmin):
    list_display = ['id', 'date_of_publication', 'description', 'get_tagged_pets']

    @staticmethod
    def get_tagged_pets(obj) -> str:
        return ','.join(pet.name for pet in obj.tagged_pets.all())
