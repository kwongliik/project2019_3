# Generated by Django 2.1.7 on 2019-04-10 12:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Inventori',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama_inventori', models.CharField(max_length=50)),
                ('harga', models.DecimalField(decimal_places=2, max_digits=5)),
                ('kuantiti', models.IntegerField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(null=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inventoris', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Pembekal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama_pembekal', models.CharField(max_length=30, unique=True)),
                ('alamat', models.CharField(max_length=100)),
                ('telefon', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Stok',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama_stok', models.CharField(max_length=30)),
                ('pembekal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stoks', to='inventori.Pembekal')),
                ('starter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stoks', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='inventori',
            name='stok',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inventoris', to='inventori.Stok'),
        ),
        migrations.AddField(
            model_name='inventori',
            name='updated_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
    ]