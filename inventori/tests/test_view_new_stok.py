from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse, resolve
from ..views import new_stok
from ..models import Pembekal, Stok
from ..forms import NewStokForm

class NewStokTests(TestCase):
    def setUp(self):
        Pembekal.objects.create(nama_pembekal='doremi S/B', alamat='kuching', telefon='2233')
        User.objects.create_user(username='john', email='john@doe.com', password='123')
        self.client.login(username='john', password='123')

    def test_new_stok_view_success_status_code(self):
        url = reverse('new_stok', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_new_stok_view_not_found_status_code(self):
        url = reverse('new_stok', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_new_stok_url_resolves_new_stok_view(self):
        view = resolve('/pembekal/1/new/')
        self.assertEquals(view.func, new_stok)

    def test_new_stok_view_contains_link_back_to_stoks_view(self):
        new_stok_url = reverse('new_stok', kwargs={'pk': 1})
        stoks_url = reverse('stoks', kwargs={'pk': 1})
        response = self.client.get(new_stok_url)
        self.assertContains(response, 'href="{0}"'.format(stoks_url))

    def test_csrf(self):
        url = reverse('new_stok', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_new_stok_valid_post_data(self):
        url = reverse('new_stok', kwargs={'pk': 1})
        data = {
            'nama_stok': 'buku'
        }
        self.client.post(url, data)
        self.assertTrue(Stok.objects.exists())

    def test_contains_form(self):  # <- new test
        url = reverse('new_stok', kwargs={'pk': 1})
        response = self.client.get(url)
        form = response.context.get('form')
        self.assertIsInstance(form, NewStokForm)

    def test_new_stok_invalid_post_data(self):
        '''
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        '''
        url = reverse('new_stok', kwargs={'pk': 1})
        response = self.client.post(url, {})
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)

    def test_new_stok_invalid_post_data_empty_fields(self):
        '''
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        '''
        url = reverse('new_stok', kwargs={'pk': 1})
        data = {
            'nama_stok': ''
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 200)
        self.assertFalse(Stok.objects.exists())

class LoginRequiredNewStokTests(TestCase):
    def setUp(self):
        Pembekal.objects.create(nama_pembekal='cemerlang s/b', alamat='sibu', telefon='334455')
        self.url = reverse('new_stok', kwargs={'pk': 1})
        self.response = self.client.get(self.url)

    def test_redirection(self):
        login_url = reverse('login')
        self.assertRedirects(self.response, '{login_url}?next={url}'.format(login_url=login_url, url=self.url))