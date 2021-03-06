# Generated by Django 2.1.4 on 2018-12-06 17:51

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('prodavnica', '0003_auto_20181206_1751'),
    ]

    operations = [
        migrations.CreateModel(
            name='Narudzbina',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ime', models.CharField(max_length=50)),
                ('prezime', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('adresa', models.CharField(max_length=250)),
                ('postanski_broj', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(99999), django.core.validators.MinValueValidator(10000)])),
                ('mesto', models.CharField(max_length=100)),
                ('kreirano', models.DateTimeField(auto_now_add=True)),
                ('azurirano', models.DateTimeField(auto_now=True)),
                ('placeno', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'narudzbine',
                'ordering': ('-kreirano',),
            },
        ),
        migrations.CreateModel(
            name='NarudzbinaPredmet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cena', models.DecimalField(decimal_places=2, max_digits=10)),
                ('kolicina', models.PositiveIntegerField(default=1)),
                ('narudzbina', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='predmeti', to='narudzbina.Narudzbina')),
                ('proizvod', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='narudzbina_predmeti', to='prodavnica.Proizvod')),
            ],
        ),
    ]
