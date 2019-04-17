from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse

from ..models import Pembekal, Stok
from ..views import StokDeleteView


class StokDeleteViewTestCase(TestCase):
    '''
    Base test case to be used in all `PostUpdateView` view tests
    '''
    def setUp(self):
        self.pembekal = Pembekal.objects.create(nama_pembekal='Peter S/B', alamat='sibu', telefon='112233')
        self.username = 'john'
        self.password = '123'
        user = User.objects.create_user(username=self.username, email='john@doe.com', password=self.password)
        self.stok = Stok.objects.create(nama_stok='buku', pembekal=self.pembekal)
        self.url = reverse('delete_stok', kwargs={
            'pk': self.pembekal.pk,
            'stok_pk': self.stok.pk,
        })

class LoginRequiredStokDeleteViewTests(StokDeleteViewTestCase):
    def test_redirection(self):
        login_url = reverse('login')
        response = self.client.get(self.url)
        self.assertRedirects(response, '{login_url}?next={url}'.format(login_url=login_url, url=self.url))

class StokDeleteViewTests(StokDeleteViewTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_class(self):
        view = resolve('/pembekal/1/stok/1/delete/')
        self.assertEquals(view.func.view_class, StokDeleteView)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_response_contains_stok_name(self):
        self.assertContains(self.response, self.stok.nama_stok)

    def test_redirection(self):
        stok_delete_response = self.client.post(self.url)
        stoks_url = reverse('stoks', kwargs={'pk':self.pembekal.pk})
        self.assertRedirects(stok_delete_response, stoks_url)