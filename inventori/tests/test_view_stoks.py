from django.test import TestCase
from django.urls import reverse, resolve
from ..views import StokListView
from ..models import Pembekal


class StoksTests(TestCase):
    def setUp(self):
        Pembekal.objects.create(nama_pembekal='ABC S/B', alamat='sibu', telefon='112233')

    def test_stoks_view_success_status_code(self):
        url = reverse('stoks', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_stoks_view_not_found_status_code(self):
        url = reverse('stoks', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_stoks_url_resolves_stoks_view(self):
        view = resolve('/pembekal/1/')
        self.assertEquals(view.func.view_class, StokListView)

    def test_stoks_view_contains_navigation_links(self):
        stoks_url = reverse('stoks', kwargs={'pk': 1})
        homepage_url = reverse('home')
        new_stok_url = reverse('new_stok', kwargs={'pk': 1})

        response = self.client.get(stoks_url)

        self.assertContains(response, 'href="{0}"'.format(homepage_url))
        self.assertContains(response, 'href="{0}"'.format(new_stok_url))