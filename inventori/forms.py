from django import forms
from .models import Stok, Inventori

class NewStokForm(forms.ModelForm):
    nama_stok = forms.CharField(
        help_text='The max length of the text is 30.'
    )
    class Meta:
        model = Stok
        fields = ['nama_stok']

class NewInventoriForm(forms.ModelForm):
    nama_inventori = forms.CharField(
        help_text='The max length of the test is 30.'
    )

    class Meta:
        model = Inventori
        fields = ['nama_inventori', 'harga', 'kuantiti',]
