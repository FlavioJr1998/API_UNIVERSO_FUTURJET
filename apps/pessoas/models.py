from django.db import models

class BaseModel ( models.Model ):
    observacao = models.CharField( max_length=300, null=True )
    data_criacao = models.DateTimeField( auto_now_add=True )
    data_atualizacao = models.DateTimeField( null=True, blank=True )

    class Meta:
        abstract = True

class PessoaFisica( BaseModel ):
    cpf = models.CharField( max_length=11, null=False )
    rg = models.CharField( max_length=20, null=False )
    def __str__(self):
        return f"CPF:{self.cpf}|RG:{self.rg}"

class PessoaJuridica( BaseModel ):
    cnpj = models.CharField( max_length=14, null=False )
    inscricao_estadual = models.CharField( max_length=9, null=False )
    def __str__(self):
        return f"CNPJ:{self.cnpj}|IE:{self.inscricao_estadual}"

class TipoPessoa( BaseModel ):
    PESSOA_FISICA = 'FISICA'
    PESSOA_JURIDICA = 'JURIDICA'
    PESSOA_CHOICES = [
        (PESSOA_FISICA, 'Física'),
        (PESSOA_JURIDICA, 'Jurídica')
    ]
    descricao = models.CharField( max_length=10, null=False, choices=PESSOA_CHOICES, default='')
    pessoa_fisica = models.ForeignKey(PessoaFisica, blank=True, null=True, on_delete=models.CASCADE, verbose_name='Pessoa Física', related_name='clientes_fisicos')
    pessoa_juridica = models.ForeignKey(PessoaJuridica, blank=True, null=True, on_delete=models.CASCADE, verbose_name='Pessoa Jurídica', related_name='clientes_juridicos')
    
    def __str__(self):
        str = ''
        if self.pessoa_fisica is not None:
            str = f"TIPO: {self.descricao}| {self.pessoa_fisica.__str__}"
        else: 
            str = f"TIPO: {self.descricao}| {self.pessoa_juridica.__str__}"
        return str
    
class Contato ( BaseModel ):
    email = models.CharField( max_length=50, null=True )
    telefone = models.CharField( max_length=20, null=False )

class Endereco ( BaseModel ):
    cep = models.CharField( max_length=10, null=False )
    rua = models.CharField( max_length=50, null=False )
    bairro = models.CharField( max_length=40, null=False)
    numero = models.CharField( max_length=10, null=False )
    complemento = models.CharField( max_length=50, null=True )
    cidade = models.CharField( max_length=20, null=False )
    estado = models.CharField( max_length=15, null=False )
    pais = models.CharField( max_length=20, null=False )

class Pessoa(BaseModel):
    tipo_pessoa = models.ForeignKey(TipoPessoa, null=False, on_delete=models.CASCADE, verbose_name="Tipo Pessoa", related_name="tipo_pessoa_cliente")
    contato = models.ForeignKey(Contato, null=False, on_delete=models.CASCADE, verbose_name='Contato', related_name='clientes_contato')
    endereco = models.ForeignKey(Endereco, null=False, on_delete=models.CASCADE, verbose_name='Endereco', related_name='clientes_endereco')

    class Meta:
        abstract = True
        
class Cliente(Pessoa):
    nome = models.CharField(max_length=50, null=False)
    ativo = models.BooleanField()
    def __str__(self):
        return f"{self.nome}"

