from rest_framework import serializers
from rest_framework.response import Response
from django.utils import timezone

from apps.financeiros.models import *

class FormaPagamentoSerializer( serializers.ModelSerializer ):
    class Meta:
        model = FormaPagmento
        fields = '__all__'

class EntradaSerializer( serializers.ModelSerializer ):
    # forma_pgmento = FormaPagamentoSerializer( read_only=True )

    class Meta:
        model = Entrada
        fields = '__all__'

    def update( self, instance, validated_data  ):   
        instance.data_atualizacao = timezone.now()
        instance.save()
        return super().update(instance, validated_data)
    
    # def create( self, validated_data ):
    #     fm_pg_instance = validated_data.get('forma_pgmento',None )
    #     validated_data['forma_pgmento'] = fm_pg_instance.pk
    #     print("$%$%$%$% CREATE ENTRADA SERIALIZER $%$%$%$%")
    #     return super().create( self, validated_data)
         
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
    tb_entrada = EntradaSerializer( read_only=False, required=False )
    tb_pgmento_financiamento = PgmentoFinanciamentoSerializer( read_only=False, required=False )
    tb_pgmento_recurso_proprio = PgmentoRecursoProprioSerializer( read_only=False, required=False )
    tb_add_implemento = AddImplementoSerializer( read_only=False, required=False )
    
    class Meta:
        model = FinanceiroProposta
        fields = '__all__'

    def create( self, validated_data ):
        preco_final = validated_data.get('preco_final', None)
        financeiro = FinanceiroProposta( preco_final=preco_final )
        tb_entrada_data = validated_data.get('tb_entrada', None) 
        if tb_entrada_data:
            fm_pg_instance = tb_entrada_data.get('forma_pgmento',None )
            tb_entrada_data['forma_pgmento'] = fm_pg_instance.pk
            entrada_serializer = EntradaSerializer( data=tb_entrada_data )
            print( entrada_serializer.is_valid( raise_exception=True ) )
            entrada_serializer.is_valid( raise_exception=True )
            entrada_serializer.save()
            financeiro.tb_entrada = entrada_serializer.instance
           
        tb_pgmento_financiamento_data = validated_data.get('tb_pgmento_financiamento',None)
        if tb_pgmento_financiamento_data:
            pgmento_financiamento_serializer = PgmentoFinanciamentoSerializer(data=tb_pgmento_financiamento_data )
            pgmento_financiamento_serializer.is_valid(raise_exception=True)
            pgmento_financiamento_serializer.save()
            financeiro.tb_pgmento_financiamento = pgmento_financiamento_serializer.instance
        
        tb_pgmento_recurso_proprio_data = validated_data.get('tb_pgmento_recurso_proprio',None)
        if tb_pgmento_recurso_proprio_data:
            fm_pg_instance = tb_pgmento_recurso_proprio_data.get('forma_pgmento',None )
            tb_pgmento_recurso_proprio_data['forma_pgmento'] = fm_pg_instance.pk
            tb_pgmento_recurso_proprio_serializer = PgmentoRecursoProprioSerializer( data=tb_pgmento_recurso_proprio_data )
            tb_pgmento_recurso_proprio_serializer.is_valid(raise_exception=True)
            tb_pgmento_recurso_proprio_serializer.save()
            financeiro.tb_pgmento_recurso_proprio = tb_pgmento_recurso_proprio_serializer.instance
        
        tb_add_implemento_data = validated_data.get('tb_add_implemento',None)
        if tb_add_implemento_data:
            tb_add_implemento_serializer = AddImplementoSerializer( data=tb_add_implemento_data )
            tb_add_implemento_serializer.is_valid(raise_exception=True)
            tb_add_implemento_serializer.save()
            financeiro.tb_add_implemento = tb_add_implemento_serializer.instance
        financeiro.save()
        return financeiro