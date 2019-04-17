from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse

from ..forms import NewInventoriForm
from ..models import Pembekal, Stok, Inventori
from ..views import new_inventori


class NewInventoriTestCase(TestCase):
    '''
    Base test case to be used in all `reply_topic` view tests
    '''
    def setUp(self):
        self.pembekal = Pembekal.objects.create(nama_pembekal='Cemerlang s/b', alamat='sibu', telefon='223344')
        self.username = 'john'
        self.password = '123'
        user = User.objects.create_user(username=self.username, email='john@doe.com', password=self.password)
        self.stok = Stok.objects.create(nama_stok='alatulis', pembekal=self.pembekal)
        Inventori.objects.create(nama_inventori='pencil', stok=self.stok, harga=1.50, kuantiti=100, created_by=user)
        self.url = reverse('new_inventori', kwargs={'pk': self.pembekal.pk, 'stok_pk': self.stok.pk})


class LoginRequiredNewInventoriTests(NewInventoriTestCase):
    def test_redirection(self):
        login_url = reverse('login')
        response = self.client.get(self.url)
        self.assertRedirects(response, '{login_url}?next={url}'.format(login_url=login_url, url=self.url))


class NewInventoriTests(NewInventoriTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_view_function(self):
        view = resolve('/pembekal/1/stok/1/new/')
        self.assertEquals(view.func, new_inventori)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, NewInventoriForm)

    def test_form_inputs(self):
        '''
        The view must contain two inputs: csrf, message textarea
        '''
        self.assertContains(self.response, '<input', 4)

class SuccessfulNewInventoriTests(NewInventoriTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.url, {'nama_inventori': 'pen', 'harga':2.00, 'kuantiti':100})

    def test_redirection(self):
        '''
        A valid form submission should redirect the user
        '''
        inventoris_url = reverse('inventoris', kwargs={'pk': self.pembekal.pk, 'stok_pk': self.stok.pk})
        self.assertRedirects(self.response, inventoris_url)

    def test_new_inventori_created(self):
        '''
        The total post count should be 2
        The one created in the `ReplyTopicTestCase` setUp
        and another created by the post data in this class
        '''
        self.assertEquals(Inventori.objects.count(), 2)


class InvalidNewInventoriTests(NewInventoriTestCase):
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
