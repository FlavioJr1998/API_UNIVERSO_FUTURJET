from rest_framework import viewsets, filters, status
from rest_framework.response import Response 
from rest_framework.utils.serializer_helpers import ReturnDict
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import api_view

from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse

from apps.pessoas.serializers import *
from apps.pessoas.models import *
from apps.financeiros.views import FinanceiroPropostaViewSet
from apps.pessoas.views import ClientesViewSet
from apps.gerador_proposta.serializers import *
from apps.gerador_proposta.models import *


class PropostasViewSet( viewsets.ModelViewSet ):
    """Listando Propostas"""
    queryset = TD_PropostaTecnicoComercial.objects.all()
    # serializer_class = PropostaSerializer
    #ADICIONANDO FILTROS
    # filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    # ordering_fields = ['nome'] #POR QUAL CAMPO SERÁ ORDENADO

    def get_serializer_class(self):
        # Use PropostaReadSerializer para requisições GET
        # Use PropostaWriteSerializer para requisições CREATE (ou POST)
        print("@@@@ get_serializer_class @@@@")
        if self.action == 'create':
            print("@@@ Entrou CREATE @@@")
            return PropostaWriteSerializer
        return PropostaReadSerializer

    def criar_ou_obter_cliente(self, dados_cliente):
        if type(dados_cliente) == dict:
            cliente_serializer = ClienteSerializer(data=dados_cliente)
            if cliente_serializer.is_valid():
                cliente = cliente_serializer.save()
                return cliente
            else:
                raise ValidationError(cliente_serializer.errors)
        else:
            print(f"$$ OBJ Cliente possui ID:{dados_cliente} $$")
            try:
                return Cliente.objects.get(id=int(dados_cliente))
            except Cliente.DoesNotExist:
                raise ValidationError({"cliente": ["Cliente não encontrado."]})

    def criar_ou_obter_financeiro(self, dados_financeiro):
        financeiro_serializer = FinanceiroPropostaSerializer(data=dados_financeiro)
        if financeiro_serializer.is_valid():
            financeiro = financeiro_serializer.save()
            return financeiro
        else:
            raise ValidationError(financeiro_serializer.errors)
    
    def create(self, request, *args, **kwargs):
        dados_proposta, dados_cliente, dados_financeiro = {}, request.data.pop("cliente", {}), request.data.pop("financeiro", {})
        cliente, financeiro = None, None
        try:
            cliente = self.criar_ou_obter_cliente(dados_cliente)
            financeiro = self.criar_ou_obter_financeiro(dados_financeiro)

            dados_proposta["cliente"] = cliente.id
            dados_proposta["financeiro"] = financeiro.id
            dados_proposta['autor'] = request.data.pop("autor", {})
            dados_proposta['versao_maquina'] = request.data.pop("versao_maquina", {})
            
            serializer = self.get_serializer(data=dados_proposta)
            
            if serializer.is_valid():
                instance = serializer.save() 
                proposta_json = PropostaReadSerializer(instance).data
                return Response(proposta_json, status=status.HTTP_201_CREATED)
            else:
                raise ValidationError(serializer.errors)
        except ValidationError as ve:
            # AJUSTAR EXCLUSÃO DO CLIENTE PARA APENAS QUANDO O ERRO FOR DO FINANCEIRO 
            if type( dados_cliente ) == dict and cliente is not None:
                    print("Excluindo cliente cadastrado na proposta invalida")
                    Cliente.objects.get(id=cliente.id).delete()

            return Response({"detail": ve.detail}, status=status.HTTP_400_BAD_REQUEST)
        
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        if serializer.is_valid(raise_exception=True):
            self.perform_update(serializer)
            cliente_data, modelo_maquina_data = request.data.pop( 'cliente', None ), request.data.pop( 'modelo_maquina', None )
            versao_maquina_data, itens_upgrade_data, alcada_liberacao_data, financeiro_data = request.data.pop( 'versao_maquina', None ), \
            request.data.pop( 'itens_upgrade', None ), request.data.pop( 'alcada_liberacao', None ), request.data.pop( 'financeiro', None )

            if cliente_data:
                tipo_pessoa_data, contato_pessoa_data, endereco_pessoa_data = cliente_data.pop('tipo_pessoa', None), cliente_data.pop('contato', None), \
                cliente_data.pop('endereco', None)

                if tipo_pessoa_data:
                    print("### Tipo Pessoa ###")
                    tipo_pessoa_instance = TipoPessoa.objects.get(id=instance.cliente.tipo_pessoa.id)
                    tipo_pessoa_serializer = TipoPessoaSerializer(tipo_pessoa_instance, data=tipo_pessoa_data, partial=True)
                    if tipo_pessoa_serializer.is_valid():
                        tipo_pessoa_serializer.save()

                if contato_pessoa_data:
                    print(f"### CONTATO PESSOA {instance.cliente.contato.id}####")
                    contato_instance = Contato.objects.get(id=instance.cliente.contato.id)
                    contato_serializer = ContatoSerializer(contato_instance, data=contato_pessoa_data, partial=True)
                    if contato_serializer.is_valid():
                        contato_serializer.save()
                
                if endereco_pessoa_data:
                    print(f"### ENDEREÇO PESSOA ###")
                    endereco_instance = Endereco.objects.get(id=instance.cliente.endereco.id)
                    endereco_serializer = EnderecoSerializer(endereco_instance, data=endereco_pessoa_data, partial=True)
                    if endereco_serializer.is_valid():
                        endereco_serializer.save()

            if modelo_maquina_data:
                print(f"####{ modelo_maquina_data}####" )
                modelo_maquina_instance = TA_Modelo.objects.get(id=instance.modelo_maquina.id)
                modelo_maquina_serializer = ModeloMaquinaSerializer(modelo_maquina_instance, data=modelo_maquina_data, partial=True)
                if modelo_maquina_serializer.is_valid():
                    modelo_maquina_serializer.save()

            if financeiro_data:
                print("#### ATUALIZANDO FINANCEIRO PROPOSTA ####")
                financeiro_instance = FinanceiroProposta.objects.get(id=instance.financeiro.id)
                financeiro_serializer = FinanceiroPropostaSerializer(financeiro_instance, data=financeiro_data, partial=True)
                if financeiro_serializer.is_valid():
                    financeiro_serializer.save()

            if versao_maquina_data:
                print("## ATUALIZANDO VERSÃO DA MÁQUINA PROPOSTA ##")
                id_versao = int(versao_maquina_data.pop('id'))
                try:
                    nova_versao = get_object_or_404(TA_Versao, id=id_versao)
                    instance.versao_maquina = nova_versao
                    instance.save()
                except Http404 as e:
                    data = {
                        'versao_maquina':'A versão informada não existe'
                    }
                    return Response(data, status=404)
            
            if itens_upgrade_data:
                print("## ATUALIZANDO ITENS UPGRADE ##")
                data_itens = TBA_ItensUpgradeVersaoMaquina.objects.filter( proposta=instance.id )
                for item in itens_upgrade_data:
                    if not data_itens.filter(item__id=item).exists():
                        print(f"## Não contem o ITEM {item} ##")
                        novo_item = TB_Item.objects.get(id=item)
                        novos_itens_upgrade = TBA_ItensUpgradeVersaoMaquina.objects.create(proposta=instance, item=novo_item)
                        novos_itens_upgrade.save() 
                data_itens = TBA_ItensUpgradeVersaoMaquina.objects.filter( proposta=instance.id )
                for item in data_itens:
                    aux_bool = False
                    for item_upgrade in itens_upgrade_data:
                        if item_upgrade == item.item.id:
                            aux_bool = True
                            break
                    if aux_bool == False:
                        TBA_ItensUpgradeVersaoMaquina.objects.get( id=item.id).delete()

            if alcada_liberacao_data:
                #CRIAR LÓGICA DE ALÇADAS
                pass

            instance.data_atualizacao = timezone.now()
            instance.save()
        return Response(serializer.data)
        
    def destroy(self, request, pk):
        #EXCLUINDO PROPOSTA
        # EXCLUIR: 'financeiro','itens_upgrade','alcadas'
        proposta_ = TD_PropostaTecnicoComercial.objects.filter( id=pk )
        if proposta_.exists():
            proposta = TD_PropostaTecnicoComercial.objects.get( id=pk )
            financeiro = FinanceiroProposta.objects.get( id=proposta.financeiro.id )
            # itens_upgrade = TCD_AlcadasProposta.objects.get(id=proposta.itens_upgrade)
            # alcadas = TCD_AlcadasProposta.objects.get(id=proposta.alcada_liberacao )
            
            FinanceiroPropostaViewSet.destroy_proposta( self, request, proposta.financeiro.id )
            proposta.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

class ModeloMaquinaViewSet( viewsets.ModelViewSet ):
    queryset = TA_Modelo.objects.all()
    serializer_class = ModeloMaquinaSerializer

    @api_view(['GET'])
    def obter_versoes_por_modelo( request, modelo_id ):
        # Obtenha o modelo com base no modelo_id (certifique-se de substituir 'SeuModelo' pelo nome do seu modelo)
        # modelo = get_object_or_404(SeuModelo, id=modelo_id)

        # Supondo que você tenha um campo de chave estrangeira chamado 'modelo' em seu modelo Versao
        versoes = TA_Versao.objects.filter(modelo_id=modelo_id)

        print( versoes )
        # Serialize as versões
        serializer = VersaoMaquinaSerializer(versoes, many=True)

        # Retorne a resposta JSON com as versões
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
    
class VersaoMaquinaViewSet( viewsets.ModelViewSet ):
    queryset = TA_Versao.objects.all()
    serializer_class = VersaoMaquinaSerializer

class ItemViewSet( viewsets.ModelViewSet ):
    queryset = TB_Item
    serializer_class = ItemSerializer

    @api_view(['GET'])
    def obter_itens_upgrade( request, bool_upgrade ):
        print( type( bool_upgrade ))
        if type(bool_upgrade) is bool:
            itens = TB_Item.objects.filter(upgrade=bool_upgrade)
            serializer = ItemSerializer(itens, many=True)
            return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
        return JsonResponse("ERRO", safe=False, status=status.HTTP_400_BAD_REQUEST)

