from django.db import models
from django.contrib.auth.models import User

class Pembekal(models.Model):
    nama_pembekal = models.CharField(max_length=30, unique=True)
    alamat = models.CharField(max_length=100)
    telefon = models.CharField(max_length=20)

    def __str__(self):
        return self.nama_pembekal


class Stok(models.Model):
    nama_stok = models.CharField(max_length=30)
    pembekal = models.ForeignKey(Pembekal, on_delete=models.CASCADE, related_name='stoks')

    def __str__(self):
        return self.nama_stok

class Inventori(models.Model):
    nama_inventori = models.CharField(max_length=50)
    stok = models.ForeignKey(Stok, on_delete=models.CASCADE, related_name='inventoris')
    harga = models.DecimalField(max_digits=5, decimal_places=2)
    kuantiti = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inventoris')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='+')

    def __str__(self):
        return self.nama_inventori
