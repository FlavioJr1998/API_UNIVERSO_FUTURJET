# Generated by Django 4.0 on 2023-12-20 20:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('financeiros', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pgmentorecursoproprio',
            name='bool_parcelado',
        ),
    ]