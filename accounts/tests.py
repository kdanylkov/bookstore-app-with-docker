from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse, resolve

from .views import SignUpPageView


class CustomUserTestCase(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
                username='will', email='will@email.com', password='testpass123'
                )
        self.assertEqual(user.username, 'will')
        self.assertEqual(user.email, 'will@email.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
                username='superadmin', email='superadmin@email.com', password='testpass123'
                )

        self.assertEqual(admin_user.username, 'superadmin')
        self.assertEqual(admin_user.email, 'superadmin@email.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)


class SignUpTestCase(TestCase):
    def setUp(self):
        self.url = reverse('signup')
        self.response = self.client.get(self.url)

    def test_template_used(self):
        self.assertTemplateUsed(self.response, 'registration/signup.html')

    def test_template_content(self):
        self.assertContains(self.response, 'Sign up page')

    def test_template_content_wrong(self):
        self.assertNotContains(self.response, 'This is a random message')

    def test_url_path_exists_at_expected_location(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_user_is_created(self):
        payload = {
                'email': 'test@email.com',
                'username': 'testusername',
                'password1': 'lordwoodJ316gdgdg5435',
                'password2': 'lordwoodJ316gdgdg5435',
                }

        self.assertEqual(get_user_model().objects.count(), 0)

        response = self.client.post(self.url, data=payload)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')
        self.assertEqual(get_user_model().objects.count(), 1)

    def test_sign_up_view_resolved_properly(self):
        view = resolve('/accounts/signup/')
        self.assertEqual(view.func.__name__, SignUpPageView.as_view().__name__)
