# Generated by Django 3.2.22 on 2024-05-29 02:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calculator', '0002_cuotasocial_cat'),
    ]

    operations = [
        migrations.CreateModel(
            name='PG_Cat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rango_min', models.FloatField()),
                ('rango_max', models.FloatField()),
                ('edad', models.FloatField()),
                ('sem1', models.FloatField()),
                ('sem2', models.FloatField()),
                ('sem3', models.FloatField()),
                ('sem4', models.FloatField()),
                ('sem5', models.FloatField()),
                ('sem6', models.FloatField()),
                ('sem7', models.FloatField()),
                ('sem8', models.FloatField()),
                ('sem9', models.FloatField()),
                ('sem10', models.FloatField()),
                ('sem11', models.FloatField()),
                ('sem12', models.FloatField()),
            ],
        ),
    ]
