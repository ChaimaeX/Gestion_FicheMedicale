# Generated by Django 5.0.4 on 2024-07-14 20:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FicheNum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('annee', models.IntegerField()),
                ('num_f', models.IntegerField()),
            ],
            options={
                'verbose_name': 'Num_Fiche',
                'verbose_name_plural': 'Num_Fiche',
            },
        ),
        migrations.CreateModel(
            name='Maladie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=132)),
                ('num_fiche', models.IntegerField()),
                ('adresse', models.CharField(max_length=200)),
                ('tel', models.IntegerField()),
                ('Observations', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'Maladie',
                'verbose_name_plural': 'Maladies',
            },
        ),
        migrations.CreateModel(
            name='FicheMedicale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('dent', models.CharField(max_length=40, null=True)),
                ('actes', models.CharField(max_length=132)),
                ('honoraires', models.CharField(max_length=132)),
                ('recu', models.CharField(max_length=132)),
                ('reste_a_paye', models.CharField(max_length=132, null=True)),
                ('maladie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.maladie')),
            ],
            options={
                'verbose_name': 'FicheMedicale',
                'verbose_name_plural': 'FicheMedicale',
            },
        ),
    ]
