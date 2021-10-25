from django.contrib import admin
from articles.models import Category, Post, postComment


# Register your models here.
admin.site.register((Category, postComment))


# Post model admin panel
class PostAdmin(admin.ModelAdmin):
    date_hierarchy = 'pub_date'
    list_filter = ('author', 'category', 'pub_date')

    # Adding custom javascript in admin panel of Post model
    class Media:
        js = ('js/slugify.js',)

admin.site.register(Post, PostAdmin)
