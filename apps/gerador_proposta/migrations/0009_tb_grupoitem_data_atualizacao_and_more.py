# Generated by Django 4.0 on 2024-02-02 18:49

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('gerador_proposta', '0008_remove_tb_grupoitem_data_atualizacao_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tb_grupoitem',
            name='data_atualizacao',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='tb_grupoitem',
            name='data_criacao',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='tb_grupoitem',
            name='observacao',
            field=models.CharField(max_length=300, null=True),
        ),
    ]
