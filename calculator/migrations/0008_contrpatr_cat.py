# Generated by Django 3.2.22 on 2024-05-29 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calculator', '0007_rentasvitalicias_cat'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContrPatr_Cat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rango_min', models.FloatField()),
                ('rango_max', models.FloatField()),
                ('y_2023', models.FloatField()),
                ('y_2024', models.FloatField()),
                ('y_2025', models.FloatField()),
                ('y_2026', models.FloatField()),
                ('y_2027', models.FloatField()),
                ('y_2028', models.FloatField()),
                ('y_2029', models.FloatField()),
                ('y_2030', models.FloatField()),
            ],
        ),
    ]