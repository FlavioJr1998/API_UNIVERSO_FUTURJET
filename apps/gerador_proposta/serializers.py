from rest_framework import serializers, status
from rest_framework.response import Response
from django.utils import timezone

from apps.gerador_proposta.models import *
from apps.gerador_proposta.validators import *
from apps.gerador_proposta.serializers import *
from apps.financeiros.serializers import * 
from apps.pessoas.serializers import ClienteSerializer

class ModeloMaquinaSerializer( serializers.ModelSerializer ):
    class Meta:
        model = TA_Modelo
        fields = ['id','descricao','tipo_maquinario','observacao']
    
    def update( self, instance, validated_data  ):   
        print("### UPDATE MODELO MAQUINA ###")
        instance.data_atualizacao = timezone.now()
        instance.save()
        return super().update(instance, validated_data)
    
class VersaoMaquinaSerializer( serializers.ModelSerializer ):
    class Meta:
        model = TA_Versao
        exclude = ['data_criacao','data_atualizacao']

    def get( self, request, *args, **kwargs ):
        print("**** METODO GET VERSAO ****")
        return Response({"message": "Método GET personalizado"}, status=status.HTTP_200_OK)
    
    def update( self, request, *args, **kwargs ):
        print("******* UPDATE VERSÃO *****")
        return Response({"message": "Método GET personalizado"}, status=status.HTTP_200_OK)
    
class AutorSerializer( serializers.ModelSerializer ):
    class Meta:
        model = User
        fields = [ 'id', 'first_name','last_name','username','email','groups' ]

class PropostaSerializer( serializers.ModelSerializer ):
    cliente = ClienteSerializer( read_only=True )
    modelo_maquina = ModeloMaquinaSerializer(read_only=True)
    versao_maquina = VersaoMaquinaSerializer( read_only=True ) #OCORRENDO ERRO NA DATA
    autor = AutorSerializer(read_only=True)
    financeiro = FinanceiroPropostaSerializer(read_only=True)
    
    class Meta:
        model = TD_PropostaTecnicoComercial
        fields = '__all__'