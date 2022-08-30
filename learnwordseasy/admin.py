from django.contrib import admin
from .models import Words, Category


class WordsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title1', 'title2', 'example2', 'category')
    list_display_links = ('id', 'title1', 'title2')
    search_fields = ('title1', 'title2', 'example2')
    list_filter = ('category',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title1')
    list_display_links = ('id', 'title1')
    search_fields = ('title1',)


admin.site.register(Words, WordsAdmin)
admin.site.register(Category, CategoryAdmin)
