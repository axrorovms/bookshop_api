from django.contrib import admin

from bookshop.models import Book, Category, Author


@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    exclude = ('page_count',)


@admin.register(Book)
class BookModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    exclude = ('page_count',)


@admin.register(Author)
class AuthorModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}







