# Generated by Django 4.0 on 2024-01-16 13:58

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('gerador_proposta', '0005_remove_ta_versao_tabela_itens_delete_tba_itensversao'),
    ]

    operations = [
        migrations.CreateModel(
            name='TBA_ItensVersao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('observacao', models.CharField(max_length=300, null=True)),
                ('data_criacao', models.DateTimeField(default=django.utils.timezone.now)),
                ('data_atualizacao', models.DateTimeField(blank=True, null=True)),
                ('quantidade', models.IntegerField(null=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='item_versao', to='gerador_proposta.tb_item')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='ta_versao',
            name='tabela_itens',
            field=models.ManyToManyField(related_name='itens_versao', through='gerador_proposta.TBA_ItensVersao', to='gerador_proposta.TB_Item'),
        ),
        migrations.AddField(
            model_name='tba_itensversao',
            name='versao_modelo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='versao_modelo', to='gerador_proposta.ta_versao'),
        ),
    ]
