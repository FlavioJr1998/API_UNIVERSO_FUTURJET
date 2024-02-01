from rest_framework import serializers, status
from rest_framework.response import Response
from django.utils import timezone

from apps.gerador_proposta.models import *
from apps.gerador_proposta.validators import *
from apps.gerador_proposta.serializers import *
from apps.financeiros.serializers import * 
from apps.pessoas.serializers import ClienteSerializer

class GrupoItemSerializer( serializers.ModelSerializer ):
    class Meta:
        model = TB_GrupoItem,
        fields = '__all__'

class ItemSerializer( serializers.ModelSerializer ):
    # grupo = GrupoItemSerializer()

    class Meta:
        model = TB_Item
        fields = '__all__'

class ModeloMaquinaSerializer( serializers.ModelSerializer ):
    class Meta:
        model = TA_Modelo
        fields = ['id','descricao','tipo_maquinario','observacao']
    
    def update( self, instance, validated_data  ):   
        print("### UPDATE MODELO MAQUINA ###")
        instance.data_atualizacao = timezone.now()
        instance.save()
        return super().update(instance, validated_data)

class ItensVersaoSerializer( serializers.ModelSerializer ):
    # item = serializers.PrimaryKeyRelatedField(queryset=TB_Item.objects.all())
    # versao_modelo = VersaoMaquinaSerializer()
    
    class Meta:
        model = TBA_ItensVersao
        fields = '__all__'

class VersaoMaquinaSerializer( serializers.ModelSerializer ):
    tabela_itens = ItemSerializer(many=True, read_only=True)
    modelo = ModeloMaquinaSerializer()

    class Meta:
        model = TA_Versao
        exclude = ['data_criacao','data_atualizacao']

class AutorSerializer( serializers.ModelSerializer ):
    class Meta:
        model = User
        fields = [ 'id', 'first_name','last_name','username','email','groups' ]

class PropostaWriteSerializer( serializers.ModelSerializer ):
    cliente = serializers.PrimaryKeyRelatedField(queryset=Cliente.objects.all())
    versao_maquina = serializers.PrimaryKeyRelatedField(queryset=TA_Versao.objects.all())
    autor = serializers.PrimaryKeyRelatedField( queryset=User.objects.all() )
    financeiro = serializers.PrimaryKeyRelatedField( queryset=FinanceiroProposta.objects.all() )
    itens_upgrade = ItemSerializer( many=True, read_only=True)

    class Meta:
        model = TD_PropostaTecnicoComercial
        fields = '__all__'

    def create(self, validated_data):
        cliente_id = validated_data.pop('cliente')
        versao_maquina_id = validated_data.pop('versao_maquina')
        autor_id = validated_data.pop('autor')
        financeiro_id = validated_data.pop('financeiro')

        proposta = TD_PropostaTecnicoComercial.objects.create(
            cliente=cliente_id,
            versao_maquina=versao_maquina_id,
            autor=autor_id,
            financeiro=financeiro_id,
            **validated_data
        )
       
        return proposta
    
class PropostaReadSerializer( serializers.ModelSerializer ):
    cliente = ClienteSerializer( read_only=False )
    versao_maquina = VersaoMaquinaSerializer( read_only=True )
    autor = AutorSerializer( read_only=True )
    financeiro = FinanceiroPropostaSerializer( read_only=True )
    itens_upgrade = ItemSerializer( many=True, read_only=True )
    
    class Meta:
        model = TD_PropostaTecnicoComercial
        fields = '__all__'
    
    