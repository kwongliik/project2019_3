from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.utils import timezone
from .forms import NewStokForm, NewInventoriForm
from .models import Pembekal, Stok, Inventori
from tablib import Dataset
from .admin import InventoriResource
from .filters import UserFilter, InventoriFilter

def inventoris_upload(request):
    if request.method == 'POST':
        inventori_resource = InventoriResource()
        dataset = Dataset()
        new_inventoris = request.FILES['myfile']

        dataset.load(new_inventoris.read())
        result = inventori_resource.import_data(dataset, dry_run=True)

        if not result.has_errors():
            inventori_resource.import_data(dataset, dry_run=False)

    return render(request, 'templates/import.html')

'''
def search_user(request):
    user_list = User.objects.all()
    user_filter = UserFilter(request.GET, queryset=user_list)
    return render(request, 'filter_user_list.html', {'filter': user_filter})

def search_inventori(request):
    inventori_list = Inventori.objects.all()
    inventori_filter = InventoriFilter(request.GET, queryset=inventori_list)
    return render(request, 'filter_inventori_list.html', {'filter': inventori_filter})'''

'''
def home(request):
    pembekals = Pembekal.objects.all()
    return render(request, 'home.html', {'pembekals':pembekals})
'''
class PembekalListView(ListView):
    model = Pembekal
    context_object_name = 'pembekals'
    template_name = 'home.html'

'''
def stoks(request, pk):
    pembekal=get_object_or_404(Pembekal, pk=pk)
    queryset = pembekal.stoks.order_by('pk')
    page = request.GET.get('page', 1)

    paginator = Paginator(queryset, 10)

    try:
        stoks = paginator.page(page)
    except PageNotAnInteger:
        # fallback to the first page
        stoks = paginator.page(1)
    except EmptyPage:
        # probably the user tried to add a page number
        # in the url, so we fallback to the last page
        stoks = paginator.page(paginator.num_pages)
    return render(request, 'stoks.html', {'pembekal':pembekal, 'stoks':stoks})
'''

class StokListView(ListView):
    model = Stok
    context_object_name = 'stoks'
    template_name = 'stoks.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        kwargs['pembekal'] = self.pembekal
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.pembekal = get_object_or_404(Pembekal, pk=self.kwargs.get('pk'))
        queryset = self.pembekal.stoks.order_by('pk')
        return queryset

@login_required
def new_stok(request, pk):
    pembekal = get_object_or_404(Pembekal, pk=pk)
    if request.method == 'POST':
        form = NewStokForm(request.POST)
        if form.is_valid():
            new_stok = form.save(commit=False)
            new_stok.pembekal = pembekal
            new_stok.save()
            return redirect('stoks', pk=pembekal.pk)  # TODO: redirect to the created topic page
    else:
        form = NewStokForm()
    return render(request, 'new_stok.html', {'pembekal': pembekal, 'form':form})

@method_decorator(login_required, name='dispatch')
class StokEditView(UpdateView):
    model = Stok
    fields = ('nama_stok',)
    template_name = 'edit_stok.html'
    pk_url_kwarg = 'stok_pk'
    context_object_name = 'stok'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def form_valid(self, form):
        stok = form.save(commit=False)
        stok.save()
        return redirect('stoks', pk=stok.pembekal.pk)


@method_decorator(login_required, name='dispatch')
class StokDeleteView(DeleteView):
    model = Stok
    template_name = 'delete_stok.html'
    pk_url_kwarg = 'stok_pk'
    context_object_name = 'stok'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get_success_url(self):
        # there is a ForeignKey from Pembekal to Stok in your model
        return reverse_lazy('stoks', kwargs={'pk': self.object.pembekal.pk})


def inventoris(request, pk, stok_pk):
    stok = get_object_or_404(Stok, pembekal__pk=pk, pk=stok_pk)
    return render(request, 'inventoris.html', {'stok': stok})

@login_required
def new_inventori(request, pk, stok_pk):
    stok = get_object_or_404(Stok, pembekal__pk=pk, pk=stok_pk)
    if request.method == 'POST':
        form = NewInventoriForm(request.POST)
        if form.is_valid():
            inventori = form.save(commit=False)
            inventori.stok = stok
            inventori.created_by = request.user
            inventori.save()
            return redirect('inventoris', pk=pk, stok_pk=stok_pk)
    else:
        form = NewInventoriForm()
    return render(request, 'new_inventori.html', {'stok': stok, 'form': form})

@method_decorator(login_required, name='dispatch')
class InventoriEditView(UpdateView):
    model = Inventori
    fields = ('nama_inventori', 'harga', 'kuantiti')
    template_name = 'edit_inventori.html'
    pk_url_kwarg = 'inventori_pk'
    context_object_name = 'inventori'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def form_valid(self, form):
        inventori = form.save(commit=False)
        inventori.updated_by = self.request.user
        inventori.updated_at = timezone.now()
        inventori.save()
        return redirect('inventoris', pk=inventori.stok.pembekal.pk, stok_pk=inventori.stok.pk)

@method_decorator(login_required, name='dispatch')
class InventoriDeleteView(DeleteView):
    model = Inventori
    template_name = 'delete_inventori.html'
    pk_url_kwarg = 'inventori_pk'
    context_object_name = 'inventori'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def get_success_url(self):
        # there is a ForeignKey from Stok to Inventori in your model
        return reverse_lazy('inventoris', kwargs={'pk': self.object.stok.pembekal.pk, 'stok_pk': self.object.stok.pk})


