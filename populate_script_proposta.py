import os, django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

import random
from apps.pessoas.models import *
from apps.financeiros.models import *
from apps.gerador_proposta.models import *
from faker_vehicle import VehicleProvider #https://pypi.org/project/faker-vehicle/
from faker import Faker #
from validate_docbr import CPF, CNPJ
import hashlib

#### ESTE ARQUIVO TEM COMO OBJETIVO POPULAR O BANCO DE DADOS COM PROPOSTAS FICTICIAS

####### FUNÇÃO PRINCIPAL ###########
def criando_propostas(quantidade):
    qtde_clientes = Cliente.objects.count()
    for _ in range(1, quantidade):
        print(f"*** Criando Proposta:{_} ****")
        cliente = retorna_cliente( qtde_clientes )
        modelo_maquinario = retorna_modelo_maquinario()
        if modelo_maquinario != False:
            versao_modelo = retorna_versao_modelo( modelo_maquinario )
            autor = retorna_autor()
            financeiro_proposta = retorna_financeiro( versao_modelo )
            try:
                proposta = TD_PropostaTecnicoComercial.objects.create(
                    cliente=cliente,
                    autor=autor,
                    modelo_maquina=modelo_maquinario,
                    versao_maquina=versao_modelo,
                    financeiro=financeiro_proposta,
                )
            except Exception as e:
                print(f"**** Erro ao gerar Proposta: {e} ******")
                return False
            print("***** SUCESSO AO GERAR PROPOSTAS *******")
        else:
            print("Cadastre pelo menos 1 maquinario no banco de dados")
            return False
    return True
####### FIM FUNÇÃO PRINCIPAL ##########   
def retorna_cliente( qtde_clientes):
    print(f"#BUSCANDO CLIENTE ALEATÓRIO#")
    while( True ):
        cliente_id = random.randint( 1, 100 )
        cliente_ = Cliente.objects.filter( id=cliente_id )
        if cliente_.exists():
            cliente = Cliente.objects.get( id=cliente_id )
            return cliente

def retorna_modelo_maquinario():
    print(f"#BUSCANDO MODELO MAQUINARIO#")
    qntde_maquinarios = ( TA_Modelo.objects.count() + 2)
    if qntde_maquinarios >= 1:
        modelo = TA_Modelo()
        while( True ):
            modelo_id = random.randint(1, qntde_maquinarios )
            modelo_ = TA_Modelo.objects.filter(id=modelo_id) 
            if modelo_.exists():
                modelo = TA_Modelo.objects.get( id=modelo_id )
                break

        return modelo
    else:
        return False

def retorna_versao_modelo( modelo ):
    print(f"#BUSCANDO VERSAO MODELO ALEATÓRIO#")
    versao, qntde_versoes_modelo = TA_Versao(),TA_Versao.objects.filter( modelo=modelo )
    if len( qntde_versoes_modelo ) > 1:
        print("### Várias Versões do modelo escolhido ###")
        while( True ):
            versoes = TA_Versao.objects.filter( modelo=modelo )
            for versao in versoes:
                bool_ = random.choice([True, False])
                if bool_:
                    return versao
    else:
        return TA_Versao.objects.get( modelo=modelo )
     
def retorna_financeiro(versao):
    #1-Entrada: 
    #   Sim: Valor | A vista ou Parcelado - Forma Pagamento
    #2-Financiamento
    #   Sim: Valor
    #3-Recurso PRoprio
    #   Sim: Valor | A vista ou Parcelado - Forma Pagamento
    #4-Add Implemento
    #   Sim: Valor - Descricao
    bool_entrada, bool_financiamento = random.choice([True, False]), random.choice([True, False]) 
    bool_rp, bool_implemento = random.choice([True, False]), random.choice([True, False])
    financeiro_proposta = FinanceiroProposta( preco_final=versao.preco_venda )

    print(f"#GERANDO FINANCEIROS#")
    if bool_entrada: #ENTRADA PROPOSTA
        print(f"#ENTRADA PROPOSTA")
        valor = random.randrange(30000, 150000)
        formas_pagamento, forma_pgmento = FormaPagmento.objects.all(), FormaPagmento()
        for fr_pg in formas_pagamento:
            if random.choice([True, False]):
                forma_pgmento = fr_pg
        
        entrada_instancia = Entrada.objects.create( valor=valor, forma_pgmento=forma_pgmento)
        financeiro_proposta.tb_entrada = entrada_instancia
    if bool_financiamento: #FINANCIAMENTO PROPOSTA
        print(f"#FINANCIAMENTO PROPOSTA")
        valor = random.randrange(30000, 300000)
        financiamento_instancia = PgmentoFinanciamento.objects.create( valor=valor )
        financeiro_proposta.tb_pgmento_financiamento = financiamento_instancia
    if bool_rp:
        print(f"#RECURSO PRÓPRIO PROPOSTA")
        valor, bool_avista, qntdade_parcelas = random.randrange(30000, 300000), random.choice([True, False]), 1
        formas_pagamento, forma_pgmento = FormaPagmento.objects.all(), FormaPagmento()
        for fr_pg in formas_pagamento:
            if random.choice([True, False]):
                forma_pgmento = fr_pg
        if bool_avista:
            qntdade_parcelas = random.randrange( 2 , 36 )
        recurso_proprio = PgmentoRecursoProprio.objects.create( valor=valor, forma_pgmento=forma_pgmento, qntdade_parcelas=qntdade_parcelas )
        financeiro_proposta.tb_pgmento_recurso_proprio = recurso_proprio
    if bool_implemento:
        print(f"#ADD IMPLEMENTO PROPOSTA")
        fake = Faker()
        fake.add_provider(VehicleProvider)
        valor,descricao = random.randrange(50000, 500000), fake.vehicle_make_model()
        implemento_add = AddImplemento.objects.create( valor=valor, descricao=descricao )
        financeiro_proposta.tb_add_implemento = implemento_add
    
    financeiro_proposta.save()
    return financeiro_proposta

def retorna_autor():
    qntde_usuarios = User.objects.count()
    cliente_id = random.randint(1, qntde_usuarios )
    return User.objects.get( id=cliente_id )

def cria_usuarios( quantidade ):
    fake = Faker('pt_BR')
    Faker.seed(10)
    print("##### CRIANDO USUÁRIOS ####")
    for _ in range(1, quantidade):
        primeiro_nome = fake.first_name()
        sobre_nome = fake.last_name()
        username = f"{primeiro_nome.lower()}.{sobre_nome.lower()}"
        email = '{}@{}'.format(username.lower(),fake.free_email_domain())
        email = email.replace(' ', '')
        senha = fake.password(length=12)
        hash = hashlib.sha256()
        hash.update(senha.encode('utf-8'))
        senha_criptografada = hash.hexdigest()

        try:
            usuario = User.objects.create( 
                password=senha_criptografada,
                is_superuser=False,
                username=username,
                first_name=primeiro_nome,
                last_name=sobre_nome,
                email=email,
                is_staff=False,
                is_active=True,
            )
        except Exception as e:
            print("*** Erro ao criar usuario: {e} ****")
            return False

def criando_clientes(quantidade_de_pessoas):
    fake = Faker('pt_BR')
    Faker.seed(10)
    print("**** GERANDO CLIENTES ****")
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
        try:
            tipo_pessoa.save()
            contato.save()
            endereco.save()
            cliente = Cliente(nome=nome, tipo_pessoa=tipo_pessoa, contato=contato, endereco=endereco, ativo=ativo)
            cliente.save()
        except Exception as e:
            print(f"**** Erro ao gerar clientes {e} ****")
            return False


##########################################
while( True ):
    quantidade_propostas, quantidade_usuarios, qtd_clientes_a_gerar, \
    quantidade_minima_clientes, quantidade_minima_usuario = 10, 10, 20, 5, 5

    if User.objects.count() > quantidade_minima_usuario: #Verifica se possui usuarios suficientes
        if Cliente.objects.count() > quantidade_minima_clientes:#Verifica se possui a qtde minima de clientes cadastrados
            criando_propostas( quantidade_propostas )
            break
        else:
            criando_clientes( qtd_clientes_a_gerar ) # Cria clientes, caso necessário
    else:
        bool_ = cria_usuarios( quantidade_usuarios ) #Cria usuarios, caso necessário
        if not bool_:
            break
