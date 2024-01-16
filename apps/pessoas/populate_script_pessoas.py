import os, django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from faker import Faker
from validate_docbr import CPF, CNPJ
import random
from apps.pessoas.models import *

def criando_pessoas(quantidade_de_pessoas):
    fake = Faker('pt_BR')
    Faker.seed(10)
    for _ in range(quantidade_de_pessoas):
        
        nome = fake.name()
        email = '{}@{}'.format(nome.lower(),fake.free_email_domain())
        email = email.replace(' ', '')
        
        celular = "{} 9{}-{}".format(random.randrange(10, 21), random.randrange(4000, 9999), random.randrange(4000, 9999))
        
        endereco = fake.address()
        linhas = endereco.split('\n')
        valores = [valor.strip() for valor in linhas[0].split(',')]
        rua = valores[0]
        numero = ''
        if valores[1]:
            numero = valores[1]
        else:
            numero = '0'
        print( linhas[1])
        bairro = linhas[1]
        cep = linhas[2].split()[0]
        cidade = ' '.join(linhas[2].split()[1:-2])
        estado = linhas[2].split()[-1]
        
        ativo = random.choice([True, False])

        tipo_pessoa = TipoPessoa()
        if _ % 2 == 0:
        #CRIANDO PESSOA FISICA
            cpf = CPF()
            cpf = cpf.generate()
            rg = "{}{}{}{}".format(random.randrange(10, 99),random.randrange(100, 999),random.randrange(100, 999),random.randrange(0, 9) ) 
            pessoa_fisica = PessoaFisica(cpf=cpf, rg=rg)
            pessoa_fisica.save()
            tipo_pessoa = TipoPessoa( descricao='FISICA', pessoa_fisica=pessoa_fisica)
        else:
        #CRIANDO PESSOA JURIDICA
            cnpj = CNPJ()
            cnpj = cnpj.generate()
            ie = "{}{}{}{}".format(random.randrange(10, 99),random.randrange(100, 999),random.randrange(100, 999),random.randrange(0, 9) ) 
            pessoa_juridica = PessoaJuridica( cnpj=cnpj, inscricao_estadual=ie )
            pessoa_juridica.save()
            tipo_pessoa = TipoPessoa( descricao='JURIDICA', pessoa_juridica=pessoa_juridica)
        
        contato = Contato(email=email, telefone=celular)
        endereco = Endereco( rua=rua, numero=numero,bairro=bairro,cep=cep, cidade=cidade,estado=estado,pais='BR')
        tipo_pessoa.save()
        contato.save()
        endereco.save()
        cliente = Cliente(nome=nome, tipo_pessoa=tipo_pessoa, contato=contato, endereco=endereco, ativo=ativo)
        cliente.save()

criando_pessoas(50)
print('Sucesso!')