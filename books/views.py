from django.views.generic import ListView, DetailView
from django.db.models import Prefetch
from django.contrib.auth.mixins import (
        LoginRequiredMixin,
        PermissionRequiredMixin
        )

from .models import Book, Review


class BookListView(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'books/book_list.html'
    context_object_name = 'book_list'
    login_url = 'account_login'


class BookDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    queryset = Book.objects.all().prefetch_related(
            Prefetch(
                'reviews',
                queryset=Review.objects.all().select_related('author')
                )
            )
    template_name = 'books/book_detail.html'
    context_object_name = 'book'
    login_url = 'account_login'
    permission_required = 'books.special_status'
