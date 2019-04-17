"""koperasi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from accounts import views as accounts_views
from inventori import views
from django_filters.views import FilterView
from inventori.filters import UserFilter, InventoriFilter

urlpatterns = [
    #path('', views.home, name='home'),
    path('', views.PembekalListView.as_view(), name='home'),
    path('signup/', accounts_views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('reset/',
        auth_views.PasswordResetView.as_view(
            template_name='password_reset.html',
            email_template_name='password_reset_email.html',
            subject_template_name='password_reset_subject.txt'
        ),
        name='password_reset'),
    path('reset/done/',
        auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
        name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
        name='password_reset_confirm'),
    path('reset/complete/',
        auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
        name='password_reset_complete'),

    path('settings/account/', accounts_views.UserUpdateView.as_view(), name='my_account'),
    path('settings/password/', auth_views.PasswordChangeView.as_view(template_name='password_change.html'),
        name='password_change'),
    path('settings/password/done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'),
        name='password_change_done'),

    path('pembekal/<int:pk>/', views.StokListView.as_view(), name='stoks'),
    path('pembekal/<int:pk>/new/', views.new_stok, name='new_stok'),
    path('pembekal/<int:pk>/stok/<int:stok_pk>/', views.inventoris, name='inventoris'),
    path('pembekal/<int:pk>/stok/<int:stok_pk>/edit/', views.StokEditView.as_view(), name='edit_stok'),
    path('pembekal/<int:pk>/stok/<int:stok_pk>/delete/', views.StokDeleteView.as_view(), name='delete_stok'),
    path('pembekal/<int:pk>/stok/<int:stok_pk>/new/', views.new_inventori, name='new_inventori'),
    path('pembekal/<int:pk>/stok/<int:stok_pk>/inventori/<int:inventori_pk>/edit/', views.InventoriEditView.as_view(), name='edit_inventori'),
    path('pembekal/<int:pk>/stok/<int:stok_pk>/inventori/<int:inventori_pk>/delete/', views.InventoriDeleteView.as_view(), name='delete_inventori'),
    #path('search_user/', views.search_user, name='search_user'),
    path('search_user/', FilterView.as_view(filterset_class=UserFilter, template_name='filter_user_list.html'), name='search_user'),
    #path('search_inventori/', views.search_inventori, name='search_inventori'),
    path('search_inventori/', FilterView.as_view(filterset_class=InventoriFilter, template_name='filter_inventori_list.html'), name='search_inventori'),
    path('admin/', admin.site.urls),
]
