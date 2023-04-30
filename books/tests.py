from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import Permission

from .models import Book, Review


class BookTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.special_status = Permission.objects.get(
                codename='special_status'
                )

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

    def test_book_list_view_for_logged_in_user(self):
        self.client.login(
                email='reviewuser@email.com',
                password='testpass123'
                )
        response = self.client.get(reverse('book_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Harry Potter')
        self.assertTemplateUsed(response, 'books/book_list.html')

    def test_book_list_view_for_logged_out_user(self):
        response = self.client.get(reverse('book_list'))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'book/book_list.html')
        login_url = reverse('account_login')
        self.assertRedirects(
                response,
                f'{login_url}?next=/books/'
                )
        response = self.client.get(f'{login_url}?next=/books/')
        self.assertContains(response, 'Log In')

    def test_book_detail_view_with_permissions(self):
        self.client.login(email='reviewuser@email.com', password='testpass123')
        self.user.user_permissions.add(self.special_status)
        response = self.client.get(self.book.get_absolute_url())
        no_response = self.client.get('/books/12324/')

        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "Harry Potter")
        self.assertContains(response, 'An excellent review')
        self.assertContains(response, 'Supercool book')
        self.assertContains(response, 'Nice one')
        self.assertTemplateUsed(response, 'books/book_detail.html')

    def test_book_detail_view_with_no_permissions(self):
        self.client.login(email='reviewuser@email.com', password='testpass123')
        response = self.client.get(self.book.get_absolute_url())
        self.assertEqual(response.status_code, 403)

    def test_amount_of_queries(self):
        self.client.login(
                email='reviewuser@email.com',
                password='testpass123'
                )
        with self.assertNumQueries(4):
            self.client.get(self.book.get_absolute_url())
