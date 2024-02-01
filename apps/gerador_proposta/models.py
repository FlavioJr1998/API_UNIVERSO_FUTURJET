from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.db import models
from django.contrib.auth.models import User
from apps.financeiros.models import FinanceiroProposta
from apps.pessoas.models import Cliente
from django.utils import timezone
#### NOMENCLATURA TABELAS #####
# MÁQUINARIO = TA 
# ITEM = TB
# ALÇADA = TC
# PROPOSTA = TD
################################

class BaseModel ( models.Model ):
    observacao = models.CharField( max_length=300, null=True )
    data_criacao = models.DateTimeField( default=timezone.now )
    data_atualizacao = models.DateTimeField( null=True, blank=True )

    class Meta:
        abstract = True 

class TA_Modelo( BaseModel ):
    TIPOS_MAQUINARIOS = [
        ("Pulverizador","Pulverizador"),
        ("Distribuidor", "Distribuidor"),
    ]
    descricao = models.CharField( max_length=50, blank=False)
    tipo_maquinario = models.CharField(max_length=20, null=False, choices=TIPOS_MAQUINARIOS, default='')

    def __str__ (self):
        return f"{self.descricao}"

class TB_GrupoItem ( BaseModel ):
    TIPOS_MAQUINARIOS = [
        ("Pulverizador","Pulverizador"),
        ("Distribuidor", "Distribuidor"),
        ("Universal", "Universal"),
    ]
    descricao = models.CharField( max_length=50, blank=False)
    tipo_maquinario = models.CharField(max_length=20, null=False, choices=TIPOS_MAQUINARIOS, default='')

    def __str__ (self):
        return f"{self.descricao}"

class TB_Item ( BaseModel ):
    descricao = models.CharField( max_length=50, blank=False)
    grupo = models.ForeignKey(
        to=TB_GrupoItem,
        on_delete=models.CASCADE,
        null=False,
        related_name="grupo_item",
    )
    preco_custo = models.BigIntegerField(blank=False)
    observacao = models.TextField(blank=True)
    upgrade = models.BooleanField( default=False )
    codigo_upgrade = models.IntegerField( null=False )

    def __str__ (self):
        return f"{self.descricao}"

class TA_Versao( BaseModel ):
    descricao = models.CharField( max_length=50, blank=False)
    preco_venda = models.BigIntegerField(blank=False)
    modelo = models.ForeignKey(
        to=TA_Modelo,
        on_delete=models.CASCADE,
        null=False,
        related_name="modelo_versao",
    )
    tabela_itens = models.ManyToManyField( TB_Item, related_name="itens_versao", through="gerador_proposta.TBA_ItensVersao")
    upgrade = models.BooleanField( default=False )
    imagem_nome = models.CharField( max_length=50, null=False)
    capa_nome = models.CharField( max_length=50, null=False)
                                            
    def __str__( self ):
        return f"{self.descricao}"

#Muitos para Muitos TB_Item <--> TA_VERSAO
class TBA_ItensVersao ( BaseModel ):
    versao_modelo = models.ForeignKey(
        to=TA_Versao,
        on_delete=models.CASCADE,
        related_name="versao_modelo"
    )
    item = models.ForeignKey(
        to=TB_Item,
        on_delete=models.CASCADE,
        related_name="item_versao"
    )
    quantidade = models.IntegerField(null=True)

class TC_TipoAlcada( BaseModel ):
    nome_alcada = models.CharField( max_length=50, null=False )
    descricao = models.CharField( max_length=50, null=False )
    responsavel_alcada = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="alcada_responsavel",
    )

class TC_AlcadaLiberacao( BaseModel ):
    # descricao_alcada = models.CharField( max_length=50 )
    tipo_alcada = models.ForeignKey(
        to=TC_TipoAlcada,
        on_delete=models.CASCADE,
        related_name="tipo_alcada"
    )
    data_leitura = models.DateTimeField( null=True, blank=True )
    data_finalizacao = models.DateTimeField( null=True )
    status_leitura = models.BooleanField( default=False )
    status_alcada = models.CharField( max_length=30, default="pendente" )
    justificativa = models.CharField( max_length=300, null=True )
    # pendente, aprovado, reprovado
    # status_alcada = models.BooleanField( default=False )

class TD_PropostaTecnicoComercial( BaseModel ):
    cliente = models.ForeignKey( Cliente, on_delete=models.CASCADE, null=False, related_name="gerador_proposta_cliente" )
    # modelo_maquina = models.ForeignKey( TA_Modelo, on_delete=models.SET_NULL, null=True,related_name="modelo_maquina_proposta" )
    versao_maquina = models.ForeignKey( TA_Versao, on_delete=models.SET_NULL, null=True, related_name="versao_maquina_proposta" )
    autor = models.ForeignKey( User, on_delete=models.SET_NULL, null=True, related_name="autor_proposta" )
    itens_upgrade = models.ManyToManyField( TB_Item, related_name="proposta_item_versao_upgrade", through="gerador_proposta.TBA_ItensUpgradeVersaoMaquina")
    alcada_liberacao = models.ManyToManyField( TC_AlcadaLiberacao, related_name="alcadas_liberacao", through="gerador_proposta.TCD_AlcadasProposta" )
    financeiro = models.ForeignKey( FinanceiroProposta, on_delete=models.CASCADE, null=False, related_name="gerador_proposta_financeiro_proposta" )
    # PERSONALIZAR O ID PARA INICIAR EM 20231001
    # INSERIR O SEGUINTE CODIGO NO MYSQL:
    # USE nome_banco; (EX: portal_futurjet)
    # ALTER TABLE nome_tabela AUTO_INCREMENT 20231001;

#Muitos para Muitos TB_Proposta <--> TB_Item
class TBA_ItensUpgradeVersaoMaquina( BaseModel ):
    proposta = models.ForeignKey(
        to=TD_PropostaTecnicoComercial,
        on_delete=models.CASCADE,
        null=False,
        related_name="proposta",
    )
    item = models.ForeignKey(
        to=TB_Item,
        on_delete=models.CASCADE,
        null=False,
        related_name="item_versao_upgrade",
    )

#Muitos para Muitos TB_PropostaComercial <--> TB_Alcada
class TCD_AlcadasProposta( BaseModel ):
    proposta = models.ForeignKey(
        to=TD_PropostaTecnicoComercial,
        on_delete=models.CASCADE,
        related_name="proposta_alcada",
    )
    alcada = models.ForeignKey(
        to=TC_AlcadaLiberacao,
        on_delete=models.CASCADE,
        related_name="alcada_proposta",
    )

# INFORMAR O NOME DO PARAMETRO EM LETRA MAISCULULA
# EX: VALOR_DESCONTO
class Parametros( BaseModel ):
    nome_parametro = models.CharField( max_length=45, null=False, unique=True )
    valor_parametro = models.CharField( max_length=50, null=False )
    descricao = models.TextField( max_length=300, null=False )

    def __str__(self):
        return self.nome_parametro

