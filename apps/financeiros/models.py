from django.db import models

##### TB'S FINANCEIRO ###########
class BaseModel ( models.Model ):
    observacao = models.CharField( max_length=100, null=True, blank=True )
    data_criacao = models.DateTimeField( auto_now_add=True )
    data_atualizacao = models.DateTimeField( null=True, blank=True )
    
    class Meta:
        abstract = True

class FormaPagmento( BaseModel ):
    FORMAS_PG_CHOICES = [
        ('DINHEIRO','dinheiro'),
        ('CHEQUE','cheque'),
        ('BOLETO','boleto'),
        ('PIX','pix'),
        ('TED','ted'),
        ('DOC','doc'),
        ('CARTÃO DE CRÉDITO','cartao de credito'),
        ('CARTÃO DE DÉBITO','cartao de debito')
    ]
    descricao = models.CharField(max_length=20, null=False, choices=FORMAS_PG_CHOICES, default='')

    def __str__(self):
        return f"{self.pk}" 
    
class Entrada ( BaseModel ):
    # ENTRADA NO NEGÓCIO
    valor = models.DecimalField( max_digits=10, decimal_places=2, null=False )
    forma_pgmento = models.ForeignKey( FormaPagmento, null=False, on_delete=models.CASCADE, related_name="entrada_forma_pagamento")

    def __str__(self):
        return f"{self.valor}"
    
class AddImplemento( BaseModel ):
    # REPRESENTA QUANDO O CLIENTE QUER INCLUIR MAQUINARIO 
    # NA NEGOCIAÇÃO
    descricao = models.CharField( max_length=50, null=False )
    valor = models.DecimalField( max_digits=12, decimal_places=2, null=True )

    def __str__(self):
        return f"{ self.descricao }"

class PgmentoFinanciamento( BaseModel ):
    # REPRESENTA VALORES FALTANTES/TOTAL DA PROPOSTA Á 
    # SEREM FINANCIADOS
    valor = models.DecimalField( max_digits=10, decimal_places=2, null=False )

    def __str__(self):
        return f"{ self.valor }"
    
class PgmentoRecursoProprio( BaseModel):
    # ESSA TABELA REPRESENTA AS ADIÇÕES DE RECURSO DO CLIENTE,
    # NÃO IMPORTANDO O MODO DE PAGAMENTO
    bool_avista = models.BooleanField( default=False )
    valor = models.DecimalField( max_digits=12, decimal_places=2, null=False )
    qntdade_parcelas = models.CharField( max_length=5, null=True )
    forma_pgmento = models.ForeignKey( FormaPagmento, null=False, on_delete=models.CASCADE, related_name="recurso_proprio_forma_pagamento")

    def __str__(self):
        return f"{ self.valor }"
    
class FinanceiroProposta( models.Model ):
    # TABELA FINANCEIRO PRINCIPAL
    tb_entrada = models.ForeignKey( Entrada, null=True, blank=True, on_delete=models.SET_NULL, related_name="financeiro_entrada") 
    tb_pgmento_financiamento = models.ForeignKey( PgmentoFinanciamento, null=True, blank=True, on_delete=models.SET_NULL, related_name="financeiro_modo_financiamento") 
    tb_pgmento_recurso_proprio = models.ForeignKey( PgmentoRecursoProprio, null=True, blank=True, on_delete=models.SET_NULL, related_name="financeiro_modo_recurso_proprio")
    tb_add_implemento = models.ForeignKey( AddImplemento, null=True, blank=True, on_delete=models.SET_NULL, related_name="financeiro_add_implemento")
    preco_final = models.DecimalField( max_digits=10, decimal_places=2, null=False )

    def __str__(self):
        return f"{ self.preco_final }"