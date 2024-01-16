from rest_framework import viewsets, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response 
import logging
from apps.pessoas.serializers import *
from apps.pessoas.models import *
from apps.financeiros.views import FinanceiroPropostaViewSet
from apps.gerador_proposta.serializers import *
from apps.gerador_proposta.models import *


class PropostasViewSet( viewsets.ModelViewSet ):
    """Listando Propostas"""
    queryset = TD_PropostaTecnicoComercial.objects.all()
    serializer_class = PropostaSerializer
    #ADICIONANDO FILTROS
    # filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    # ordering_fields = ['nome'] #POR QUAL CAMPO SERÁ ORDENADO

    # def get_serializer_class(self):
    #   if self.request.version == '2':
    #     return ClienteSerializerV2
    #   else:
    #     return ClienteSerializer

    # def create(self, request):
    #     tipo_pessoa_data = request.data['tipo_pessoa']
    #     contato_data = request.data['contato']
    #     endereco_data = request.data['endereco']
    #     dados_simples = {chave: valor for chave, valor in request.data.items() if not isinstance(valor, dict)}
    #     cliente_data = {
    #         'tipo_pessoa': tipo_pessoa_data,
    #         'contato': contato_data,
    #         'endereco': endereco_data,
    #         **dados_simples
    #     }
    #     serializer = ClienteSerializer(data=cliente_data)

    #     if serializer.is_valid():
    #         serializer.save()
    #         response_data = serializer.data
    #         response = Response(response_data, status=status.HTTP_201_CREATED)
    #         id = str(serializer.data['id'])
    #         response['Location'] = request.build_absolute_uri() + id
    #         return response
    #     else:
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def update(self, request, pk):
    #     print("@@@@@@ cHEGOU NO PATCH @@@@@@")
    #     logger = logging.getLogger(__name__)
    #     logger.debug(f'Dados recebidos: {request.data}')
    #     proposta = self.get_object(pk)
    #     serializer = self.get_serializer(proposta, data=request.data, partial=True)
        
    #     cliente_data = request.pop('cliente', None)
    #     if cliente_data:
    #         cliente_serializer = ClienteSerializer(request.cliente, data=cliente_data, partial=True)
    #         if cliente_serializer.is_valid():
    #             cliente_serializer.save()
            
    #     if serializer.is_valid():
    #         serializer.save()

    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        print( request.data )
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
                print("#### FINANCEIRO ####")
                financeiro_instance = FinanceiroProposta.objects.get(id=instance.financeiro.id)
                financeiro_serializer = FinanceiroPropostaSerializer(financeiro_instance, data=financeiro_data, partial=True)
                if financeiro_serializer.is_valid():
                    financeiro_serializer.save()

            if versao_maquina_data:
                print("## VERSAO MAQUINA ##")
                
            if itens_upgrade_data:
                pass
            if alcada_liberacao_data:
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
    

