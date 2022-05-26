from django.contrib import admin
from .models import *

class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    list_display_links = ('name', )
    search_fields = ('name', )
    prepopulated_fields = {'slug': ('name', )}


admin.site.register(Genre, GenreAdmin)
admin.site.register(Novella)
admin.site.register(Comment)