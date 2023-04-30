from django.views.generic import ListView, DetailView
from django.db.models import Prefetch

from .models import Book, Review


class BookListView(ListView):
    model = Book
    template_name = 'books/book_list.html'
    context_object_name = 'book_list'


class BookDetailView(DetailView):
    queryset = Book.objects.all().prefetch_related(
            Prefetch(
                'reviews',
                queryset=Review.objects.all().select_related('author')
                )
            )
    template_name = 'books/book_detail.html'
    context_object_name = 'book'
