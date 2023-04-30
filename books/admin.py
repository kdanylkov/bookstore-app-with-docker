from django.contrib import admin

from .models import Book, Review


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'price')
    list_display_links = ('title',)
    inlines = [
            ReviewInline,
            ]
