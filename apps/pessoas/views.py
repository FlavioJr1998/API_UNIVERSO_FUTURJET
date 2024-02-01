from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from datetime import datetime
from apps.pessoas.serializers import ClienteSerializer, ClienteSerializerV2
from apps.pessoas.models import *
from django_filters.rest_framework import DjangoFilterBackend
import logging

class ClientesViewSet(viewsets.ModelViewSet):
    """Listando clientes"""
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    #ADICIONANDO FILTROS
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['nome'] #POR QUAL CAMPO SERÁ ORDENADO
    lookup_field = 'pk'  # Adicionando o lookup_field
  
    def get_serializer_class(self):
      if self.request.version == '2':
        return ClienteSerializerV2
      else:
        return ClienteSerializer

    def criar_tipo_pessoa(self, tipo_pessoa_data):
        descricao = tipo_pessoa_data['descricao']
        tipo_pessoa_instance = TipoPessoa(descricao=descricao)
        
        if descricao == 'FISICA':
            pessoa_fisica_instance = PessoaFisica.objects.create(
                cpf=tipo_pessoa_data['pessoa_fisica']['cpf'],
                rg=tipo_pessoa_data['pessoa_fisica']['rg']
            )
            tipo_pessoa_instance.pessoa_fisica = pessoa_fisica_instance
        elif descricao == 'JURIDICA':
            pessoa_juridica_instance = PessoaJuridica.objects.create(
                cnpj=tipo_pessoa_data['pessoa_juridica']['cnpj'],
                inscricao_estadual=tipo_pessoa_data['pessoa_juridica']['inscricao_estadual']
            )
            tipo_pessoa_instance.pessoa_juridica = pessoa_juridica_instance

        tipo_pessoa_instance.save()
        return tipo_pessoa_instance
    
    def create( self, request ):
        tipo_pessoa_data = request.data['tipo_pessoa']
        contato_data = request.data['contato']
        endereco_data = request.data['endereco']
        dados_simples = {chave: valor for chave, valor in request.data.items() if not isinstance(valor, dict)}
        cliente_data = {
            'tipo_pessoa': tipo_pessoa_data,
            'contato': contato_data,
            'endereco': endereco_data,
            **dados_simples
        }
        serializer = ClienteSerializer(data=cliente_data)

        if serializer.is_valid():
            serializer.save()
            response_data = serializer.data
            response = Response(response_data, status=status.HTTP_201_CREATED)
            id = str(serializer.data['id'])
            response['Location'] = request.build_absolute_uri() + id
            return response
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        print("@#@#@#@#@#@# PATCH @#@#@#@#@#@#@#@#")
        logger = logging.getLogger(__name__)
        logger.debug(f'Dados recebidos: {request.data}')
        cliente = self.get_object(pk)
        serializer = self.get_serializer(cliente, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        instance.data_atualizacao = datetime.now()
        instance.save()
        return Response(serializer.data)

    def destroy(self, request, pk):
        print("#############33 PASSOU #############")
        cliente = Cliente.objects.get( id=pk )
        tipo_pessoa = TipoPessoa.objects.get(id=cliente.tipo_pessoa.id )
        contato = Contato.objects.get(id=cliente.contato.id)
        endereco = Endereco.objects.get(id=cliente.endereco.id)
        tipo_pessoa.delete()
        contato.delete()
        endereco.delete()
        cliente.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    