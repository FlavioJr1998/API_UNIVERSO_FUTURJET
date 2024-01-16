from rest_framework import serializers
from rest_framework.response import Response
from django.utils import timezone
from apps.pessoas.models import Cliente, TipoPessoa, Contato, Endereco, PessoaFisica, PessoaJuridica
from apps.pessoas.validators import *


class PessoaFisicaSerializer( serializers.ModelSerializer):
    class Meta:
        model = PessoaFisica
        exclude = ['id','observacao', 'data_criacao','data_atualizacao']
    
    def validate(self, data):
        cpf, rg = data.get('cpf', None ), data.get('rg', None ) 
        if cpf is not None and not verificar_cpf( cpf ):
            raise serializers.ValidationError({'cpf': "Número de CPF inválido!"})

        if rg is not None and not verificar_rg(rg):
            raise serializers.ValidationError({'rg': "O RG deve conter 9 dígitos!"})
        return data

class PessoaJuridicaSerializer( serializers.ModelSerializer):
    class Meta:
        model = PessoaJuridica
        exclude = ['id','observacao', 'data_criacao','data_atualizacao']
    
    def validate(self, data):
        cnpj, inscricao_estadual = data.get( 'cnpj', None ), data.get( 'inscricao_estadual', None ) 
        if cnpj is not None and not verificar_cnpj( cnpj ):
            raise serializers.ValidationError({'cnpj': "Número de CNPJ inválido!"})

        if inscricao_estadual is not None and not verificar_inscricao_estadual( inscricao_estadual ):
            raise serializers.ValidationError({'inscricao_estadual': "A IE deve conter 9 dígitos!"})
        return data
    
class TipoPessoaSerializer(serializers.ModelSerializer):
    pessoa_fisica = PessoaFisicaSerializer( required=False )
    pessoa_juridica = PessoaJuridicaSerializer( required=False )

    class Meta:
        model = TipoPessoa
        exclude = ['id','observacao', 'data_criacao','data_atualizacao']

    def to_representation(self, instance):
        representation = super(TipoPessoaSerializer, self).to_representation(instance)

        representation.pop('pessoa_juridica', None) #RETIRANDO A COLUNA DE EXIBIÇÃO
        representation.pop('pessoa_fisica', None) 

        # Adiciona a chave estrangeira não nula ao JSON
        if instance.pessoa_fisica:
            representation['pessoa'] = PessoaFisicaSerializer(instance.pessoa_fisica).data
        elif instance.pessoa_juridica:
            representation['pessoa'] = PessoaJuridicaSerializer(instance.pessoa_juridica).data
            

        return representation
    
    def create(self, validated_data):
        pessoa_fisica_data = validated_data.get('pessoa_fisica', {})
        pessoa_juridica_data = validated_data.get('pessoa_juridica', {})
        descricao = validated_data['descricao']

        pessoa_fisica, pessoa_juridica = None, None

        if pessoa_fisica_data and descricao == 'FISICA':
            pessoa_fisica_serializer = PessoaFisicaSerializer(data=pessoa_fisica_data)
            pessoa_fisica_serializer.is_valid(raise_exception=True)
            pessoa_fisica = pessoa_fisica_serializer.save()

        elif pessoa_juridica_data and descricao == 'JURIDICA':
            pessoa_juridica_serializer = PessoaJuridicaSerializer(data=pessoa_juridica_data)
            pessoa_juridica_serializer.is_valid(raise_exception=True)
            pessoa_juridica = pessoa_juridica_serializer.save()

        tipo_pessoa = TipoPessoa(descricao=descricao, pessoa_fisica=pessoa_fisica, pessoa_juridica=pessoa_juridica)
        tipo_pessoa.save()

        return tipo_pessoa

    def update(self, instance, validated_data):
        print( f"00000000000000|{validated_data}|00000000000000" )
        tipo_pessoa_data, pessoa_fisica_data, pessoa_juridica_data = '', validated_data.pop('pessoa_fisica', None), validated_data.pop('pessoa_juridica', None)
        if pessoa_fisica_data:
            pessoa_fisica_serializer = PessoaFisicaSerializer(instance.pessoa_fisica, data=pessoa_fisica_data, partial=True)
            if pessoa_fisica_serializer.is_valid(raise_exception=True):
                if not instance.pessoa_fisica:
                    cpf = pessoa_fisica_data.pop('cpf')
                    rg = pessoa_fisica_data.pop('rg')
                    instance.pessoa_fisica = PessoaFisica.objects.create(cpf=cpf, rg=rg)
                
                instance.pessoa_fisica.data_atualizacao = timezone.now()
                instance.data_atualizacao = timezone.now()
                instance.descricao = 'FISICA'
                
                pessoa_juridica_instance = instance.pessoa_juridica
                if pessoa_juridica_instance:
                    pessoa_juridica_instance.save()
                    # Desvincule pessoa_juridica de instance antes de excluir
                    instance.pessoa_juridica = None
                    instance.save()  # Salve a instância para remover a referência à pessoa_juridica
                    pessoa_juridica_instance.delete()
                instance.save()
                tipo_pessoa_data = pessoa_fisica_serializer.save()
        elif pessoa_juridica_data:
            pessoa_juridica_serializer = PessoaJuridicaSerializer(instance.pessoa_juridica, data=pessoa_juridica_data, partial=True)
            print("4444444444444")
            if pessoa_juridica_serializer.is_valid(raise_exception=True):
                if not instance.pessoa_juridica:
                    instance.pessoa_juridica = PessoaJuridica.objects.create(cnpj=pessoa_juridica_data.pop('cnpj'), inscricao_estadual=pessoa_juridica_data.pop('inscricao_estadual'))
                
                instance.data_atualizacao = timezone.now()
                instance.descricao = 'JURIDICA'
                if instance.pessoa_fisica:
                    print(f"****** {instance.pessoa_fisica }******")
                    pessoa_fisica_instance = PessoaFisica.objects.get( id=instance.pessoa_fisica.id )
                    # Desvincule pessoa_juridica de instance antes de excluir
                    instance.pessoa_fisica = None
                    pessoa_fisica_instance.delete()      
                instance.save()
                tipo_pessoa_data = pessoa_juridica_serializer.save()    
        
        return Response(tipo_pessoa_data)
        # return super().update(instance, validated_data)

class ContatoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contato
        fields = '__all__'

    def validate(self, data):
        email, telefone = data.get('email', None), data.get('telefone', None)

        if email is not None and not verificar_email( email ):
            raise serializers.ValidationError({'email': f"Email inválido" })
        if telefone and not verificar_celular( telefone ):
            raise serializers.ValidationError({'telefone': f"O número de celular deve seguir o seguinte padrão (44)91234-1234!|"})
        return data
    
    def update( self, instance, validated_data ):
        print("### UPDATE CONTATO ###")
        instance.data_atualizacao = timezone.now()
        instance.save()
        return super().update(instance, validated_data)
    
class EnderecoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endereco
        exclude = ['id','observacao', 'data_criacao','data_atualizacao']
    
class ClienteSerializer(serializers.ModelSerializer):
    tipo_pessoa = TipoPessoaSerializer( )
    contato = ContatoSerializer()
    endereco = EnderecoSerializer()

    class Meta:
        model = Cliente
        fields = '__all__'

    def validate(self, data):
        nome = data.get( 'nome', None ) 
        if nome is not None and not verificar_nome( nome ):
            raise serializers.ValidationError({'nome': f"O nome não deve conter números!"})
        return data
    
    def update( self, instance, validated_data ):
        print(f"***** Validate data Cliente: {validated_data} *******")
        contato_data = validated_data.pop('contato', None)
        if contato_data:
            contato_serializer = ContatoSerializer(instance.contato, data=contato_data, partial=True)
            contato_serializer.is_valid(raise_exception=True)
            contato_serializer.save()
        endereco_data = validated_data.pop('endereco',None)
        if endereco_data:
            endereco_serializer = EnderecoSerializer(instance.endereco, data=endereco_data, partial=True)
            endereco_serializer.is_valid(raise_exception=True)
            endereco_serializer.save()
        tipo_pessoa_data = validated_data.pop('tipo_pessoa',None)
        if tipo_pessoa_data:
            tipo_pessoa_serializer = TipoPessoaSerializer(instance.tipo_pessoa, data=tipo_pessoa_data, partial=True)
            tipo_pessoa_serializer.is_valid(raise_exception=True)
            tipo_pessoa_serializer.save()

        return super().update(instance, validated_data)
        

class ClienteSerializerV2(serializers.ModelSerializer):
    tipo_pessoa = TipoPessoaSerializer()
    contato = ContatoSerializer()
    endereco = EnderecoSerializer()

    class Meta:
        model = Cliente
        fields = '__all__'

    def validate(self, data):
        if not verificar_nome(data['nome']):
            raise serializers.ValidationError({'nome': f"O nome não deve conter números!{ verificar_nome(data['nome']) }"})

        if not verificar_celular(data['contato']['telefone']):
            raise serializers.ValidationError({'celular': "O número de celular deve seguir o seguinte padrão (44)91234-1234!"})

        
        return data

"""
Os serializadores permitem que dados complexos, como conjuntos de consultas e instâncias de modelo, sejam convertidos em tipos de dados nativos do Python que podem ser facilmente renderizados em JSON, XMLou em outros tipos de conteúdo. Os serializadores também fornecem desserialização, permitindo que os dados analisados ​​sejam convertidos novamente em tipos complexos, após primeiro validar os dados recebidos.

Os serializadores no framework REST funcionam de forma muito semelhante aos do Django Forme ModelFormàs classes. Fornecemos uma Serializerclasse que oferece uma maneira poderosa e genérica de controlar a saída de suas respostas, bem como uma ModelSerializerclasse que fornece um atalho útil para criar serializadores que lidam com instâncias de modelo e conjuntos de consultas.
"""