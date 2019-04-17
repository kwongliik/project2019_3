from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse

from ..models import Pembekal, Stok, Inventori
from ..views import InventoriDeleteView


class InventoriDeleteViewTestCase(TestCase):
    '''
    Base test case to be used in all `PostUpdateView` view tests
    '''
    def setUp(self):
        self.pembekal = Pembekal.objects.create(nama_pembekal='Peter S/B', alamat='sibu', telefon='112233')
        self.username = 'john'
        self.password = '123'
        user = User.objects.create_user(username=self.username, email='john@doe.com', password=self.password)
        self.stok = Stok.objects.create(nama_stok='buku', pembekal=self.pembekal)
        self.inventori = Inventori.objects.create(nama_inventori='buku latihan', stok=self.stok, harga=2.00, kuantiti=100, created_by=user)
        self.url = reverse('delete_inventori', kwargs={
            'pk': self.pembekal.pk,
            'stok_pk': self.stok.pk,
            'inventori_pk': self.inventori.pk
        })


class LoginRequiredInventoriDeleteViewTests(InventoriDeleteViewTestCase):
    def test_redirection(self):
        login_url = reverse('login')
        response = self.client.get(self.url)
        self.assertRedirects(response, '{login_url}?next={url}'.format(login_url=login_url, url=self.url))


class UnauthorizedInventoriDeleteViewTests(InventoriDeleteViewTestCase):
    def setUp(self):
        super().setUp()
        username = 'jane'
        password = '321'
        User.objects.create_user(username=username, email='jane@doe.com', password=password)
        self.client.login(username=username, password=password)
        self.response = self.client.get(self.url)

    def test_status_code(self):
        '''
        A topic should be edited only by the owner.
        Unauthorized users should get a 404 response (Page Not Found)
        '''
        self.assertEquals(self.response.status_code, 404)


class InventoriDeleteViewTests(InventoriDeleteViewTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_class(self):
        view = resolve('/pembekal/1/stok/1/inventori/1/delete/')
        self.assertEquals(view.func.view_class, InventoriDeleteView)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_response_contains_inventori_name(self):
        self.assertContains(self.response, self.inventori.nama_inventori)

    def test_redirection(self):
        inventori_delete_response = self.client.post(self.url)
        inventoris_url = reverse('inventoris', kwargs={'pk':self.pembekal.pk, 'stok_pk':self.stok.pk})
        self.assertRedirects(inventori_delete_response, inventoris_url)


