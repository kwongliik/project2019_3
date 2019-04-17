from django.forms import ModelForm
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse

from ..models import Pembekal, Stok
from ..views import StokEditView


class StokEditViewTestCase(TestCase):
    '''
    Base test case to be used in all `StokEditView` view tests
    '''
    def setUp(self):
        self.pembekal = Pembekal.objects.create(nama_pembekal='Peter S/B', alamat='sibu', telefon='112233')
        self.username = 'john'
        self.password = '123'
        self.stok = Stok.objects.create(nama_stok='buku', pembekal=self.pembekal)
        self.url = reverse('edit_stok', kwargs={
            'pk': self.pembekal.pk,
            'stok_pk': self.stok.pk
        })

class LoginRequiredStokEditViewTests(StokEditViewTestCase):
    def test_redirection(self):
        login_url = reverse('login')
        response = self.client.get(self.url)
        self.assertRedirects(response, '{login_url}?next={url}'.format(login_url=login_url, url=self.url))

class StokEditViewTests(StokEditViewTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_class(self):
        view = resolve('/pembekal/1/stok/1/edit/')
        self.assertEquals(view.func.view_class, StokEditView)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, ModelForm)

    def test_form_inputs(self):
        '''
        The view must contain four inputs: csrf, nama_stok
        '''
        self.assertContains(self.response, '<input', 2)