# Generated by Django 4.0 on 2023-12-20 20:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('financeiros', '0002_remove_pgmentorecursoproprio_bool_parcelado'),
    ]

    operations = [
        migrations.AddField(
            model_name='financeiroproposta',
            name='tb_entrada',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='financeiro_entrada', to='financeiros.entrada'),
        ),
    ]