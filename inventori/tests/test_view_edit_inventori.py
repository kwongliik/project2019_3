from django.forms import ModelForm
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse

from ..models import Pembekal, Stok, Inventori
from ..views import InventoriEditView


class InventoriEditViewTestCase(TestCase):
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
        self.url = reverse('edit_inventori', kwargs={
            'pk': self.pembekal.pk,
            'stok_pk': self.stok.pk,
            'inventori_pk': self.inventori.pk
        })


class LoginRequiredInventoriEditViewTests(InventoriEditViewTestCase):
    def test_redirection(self):
        login_url = reverse('login')
        response = self.client.get(self.url)
        self.assertRedirects(response, '{login_url}?next={url}'.format(login_url=login_url, url=self.url))


class UnauthorizedInventoriEditViewTests(InventoriEditViewTestCase):
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


class InventoriEditViewTests(InventoriEditViewTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_class(self):
        view = resolve('/pembekal/1/stok/1/inventori/1/edit/')
        self.assertEquals(view.func.view_class, InventoriEditView)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, ModelForm)

    def test_form_inputs(self):
        '''
        The view must contain four inputs: csrf, nama_inventori, harga and kuantiti
        '''
        self.assertContains(self.response, '<input', 4)


class SuccessfulInventoriEditViewTests(InventoriEditViewTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.url, {'nama_inventori': 'buku latihan', 'stok': self.stok, 'harga': '3.00', 'kuantiti': '200'})

    def test_redirection(self):
        '''
        A valid form submission should redirect the user
        '''
        inventoris_url = reverse('inventoris', kwargs={'pk': self.pembekal.pk, 'stok_pk': self.stok.pk})
        self.assertRedirects(self.response, inventoris_url)

    def test_inventori_changed(self):
        self.inventori.refresh_from_db()
        self.assertEquals(self.inventori.nama_inventori, 'buku latihan')


class InvalidInventoriEditViewTests(InventoriEditViewTestCase):
    def setUp(self):
        '''
        Submit an empty dictionary to the `reply_topic` view
        '''
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.url, {})

    def test_status_code(self):
        '''
        An invalid form submission should return to the same page
        '''
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)