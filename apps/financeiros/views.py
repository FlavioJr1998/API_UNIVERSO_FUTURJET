from rest_framework import viewsets, filters, status
from apps.gerador_proposta.serializers import *
from apps.gerador_proposta.models import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response 
from django.shortcuts import get_object_or_404

class FinanceiroPropostaViewSet(viewsets.ModelViewSet):
    """Listando clientes"""
    
    queryset = FinanceiroProposta.objects.all()
    serializer_class = FinanceiroPropostaSerializer
    #ADICIONANDO FILTROS
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['nome'] #POR QUAL CAMPO SERÁ ORDENADO
    lookup_field = 'pk'  # Adicionando o lookup_field
  
    # def get_serializer_class(self):
    #   if self.request.version == '2':
    #     return ClienteSerializerV2
    #   else:
    #     return ClienteSerializer

    # def criar_tipo_pessoa(self, tipo_pessoa_data):
    #     descricao = tipo_pessoa_data['descricao']
    #     tipo_pessoa_instance = TipoPessoa(descricao=descricao)
        
    #     if descricao == 'FISICA':
    #         pessoa_fisica_instance = PessoaFisica.objects.create(
    #             cpf=tipo_pessoa_data['pessoa_fisica']['cpf'],
    #             rg=tipo_pessoa_data['pessoa_fisica']['rg']
    #         )
    #         tipo_pessoa_instance.pessoa_fisica = pessoa_fisica_instance
    #     elif descricao == 'JURIDICA':
    #         pessoa_juridica_instance = PessoaJuridica.objects.create(
    #             cnpj=tipo_pessoa_data['pessoa_juridica']['cnpj'],
    #             inscricao_estadual=tipo_pessoa_data['pessoa_juridica']['inscricao_estadual']
    #         )
    #         tipo_pessoa_instance.pessoa_juridica = pessoa_juridica_instance

    #     tipo_pessoa_instance.save()
    #     return tipo_pessoa_instance
    
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

    # def patch(self, request, pk):
    #     logger = logging.getLogger(__name__)
    #     logger.debug(f'Dados recebidos: {request.data}')
    #     cliente = self.get_object(pk)
    #     serializer = self.get_serializer(cliente, data=request.data, partial=True)

    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)

    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        financeiro = get_object_or_404(FinanceiroProposta, id=pk)

        exclusao( self, pk, financeiro )
        financeiro.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def destroy_proposta(self, request, pk):
        financeiro = FinanceiroProposta.objects.filter(id=pk)
        if financeiro.exists():
            exclusao( self, pk, FinanceiroProposta.objects.get(id=pk) )
            return True
        else:
            return False

def exclusao( self, pk, financeiro ):
    if financeiro.tb_entrada:
        financeiro.tb_entrada.delete()
    if financeiro.tb_pgmento_recurso_proprio:
        financeiro.tb_pgmento_recurso_proprio.delete()
    if financeiro.tb_pgmento_financiamento:
        financeiro.tb_pgmento_financiamento.delete()
    if financeiro.tb_add_implemento:
        financeiro.tb_add_implemento.delete()
    
        