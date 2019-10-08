from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Post, Category

# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'author')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'publish'

admin.site.register(Category , MPTTModelAdmin)