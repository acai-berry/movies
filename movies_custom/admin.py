from django.contrib import admin
from movies_app.admin import FilmAdmin
from movies_app.models import Film
from tags.models import TaggedItem
from django.contrib.contenttypes.admin import GenericTabularInline

# Register your models here.
class TagInLine(GenericTabularInline):
    autocomplete_fields = ['tag']
    model = TaggedItem


class CustomFilmAdmin(FilmAdmin):
    inlines = [TagInLine]

admin.site.unregister(Film)
admin.site.register(Film, CustomFilmAdmin)

