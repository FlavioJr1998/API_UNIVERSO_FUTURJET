from rest_framework import serializers
from rest_framework.response import Response
from django.utils import timezone

from apps.financeiros.models import *

class EntradaSerializer( serializers.ModelSerializer ):
    class Meta:
        model = Entrada
        fields = ['id','valor','forma_pgmento']

    def update( self, instance, validated_data  ):   
        instance.data_atualizacao = timezone.now()
        instance.save()
        return super().update(instance, validated_data)
    
class AddImplementoSerializer( serializers.ModelSerializer ):
    class Meta:
        model = AddImplemento
        fields = ['id','valor','descricao']

    def update( self, instance, validated_data  ):   
        instance.data_atualizacao = timezone.now()
        instance.save()
        return super().update(instance, validated_data)
    
class PgmentoFinanciamentoSerializer( serializers.ModelSerializer ):
    class Meta:
        model = PgmentoFinanciamento
        fields = ['id','valor']

    def update( self, instance, validated_data  ):   
        instance.data_atualizacao = timezone.now()
        instance.save()
        return super().update(instance, validated_data)
    
class PgmentoRecursoProprioSerializer( serializers.ModelSerializer ):
    class Meta:
        model = PgmentoRecursoProprio
        exclude = ['data_criacao', 'data_atualizacao']

    def update( self, instance, validated_data  ):   
        instance.data_atualizacao = timezone.now()
        instance.save()
        return super().update(instance, validated_data)
    
class FinanceiroPropostaSerializer( serializers.ModelSerializer ):
    tb_entrada = EntradaSerializer( read_only=True )
    tb_pgmento_financiamento = PgmentoFinanciamentoSerializer( read_only=True )
    tb_pgmento_recurso_proprio = PgmentoRecursoProprioSerializer( read_only=True )
    tb_add_implemento = AddImplementoSerializer( read_only=True )
    
    class Meta:
        model = FinanceiroProposta
        fields = '__all__'