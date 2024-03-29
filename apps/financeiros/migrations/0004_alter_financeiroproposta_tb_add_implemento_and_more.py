# Generated by Django 4.0 on 2024-01-29 13:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('financeiros', '0003_financeiroproposta_tb_entrada'),
    ]

    operations = [
        migrations.AlterField(
            model_name='financeiroproposta',
            name='tb_add_implemento',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='financeiro_add_implemento', to='financeiros.addimplemento'),
        ),
        migrations.AlterField(
            model_name='financeiroproposta',
            name='tb_entrada',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='financeiro_entrada', to='financeiros.entrada'),
        ),
        migrations.AlterField(
            model_name='financeiroproposta',
            name='tb_pgmento_financiamento',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='financeiro_modo_financiamento', to='financeiros.pgmentofinanciamento'),
        ),
        migrations.AlterField(
            model_name='financeiroproposta',
            name='tb_pgmento_recurso_proprio',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='financeiro_modo_recurso_proprio', to='financeiros.pgmentorecursoproprio'),
        ),
    ]
