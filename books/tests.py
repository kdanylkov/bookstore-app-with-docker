from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Book, Review


class BookTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
                username='reviewuser',
                email='reviewuser@email.com',
                password='testpass123'
                )

        cls.book = Book.objects.create(
                title='Harry Potter',
                author='JK Rowling',
                price='25.00'
                )
        cls.review1 = Review.objects.create(
                book=cls.book,
                author=cls.user,
                review='An excellent review'
                )
        cls.review2 = Review.objects.create(
                book=cls.book,
                author=cls.user,
                review='Supercool book'
                )
        cls.review3 = Review.objects.create(
                book=cls.book,
                author=cls.user,
                review='Nice one'
                )

    def test_books_listing(self):
        self.assertEqual(f'{self.book.title}', 'Harry Potter')
        self.assertEqual(f'{self.book.author}', 'JK Rowling')
        self.assertEqual(f'{self.book.price}', '25.00')

    def test_book_list_view(self):
        response = self.client.get(reverse('book_list'))
        self.assertContains(response, 'Harry Potter')
        self.assertTemplateUsed(response, 'books/book_list.html')

    def test_book_detail_view(self):
        response = self.client.get(self.book.get_absolute_url())
        no_response = self.client.get('/books/12324/')

        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "Harry Potter")
        self.assertContains(response, 'An excellent review')
        self.assertContains(response, 'Supercool book')
        self.assertContains(response, 'Nice one')
        self.assertTemplateUsed(response, 'books/book_detail.html')

    def test_amount_of_queries(self):
        with self.assertNumQueries(2):
            self.client.get(self.book.get_absolute_url())
