from validate_docbr import CPF
import re

def verificar_cpf( numero_cpf ): #VALIDANDO CPF, PARA QUE POSSUA 11 DIGITOS 
    cpf = CPF()
    return cpf.validate( numero_cpf )

def verificar_rg( rg ): #VALIDANDO RG, PARA QUE POSSUA 9 DIGITOS
    return len( rg ) == 9

def verificar_nome( nome ): #VALIDANDO NOME, PARA QUE NÃO POSSUA NÚMEROS 
    return nome.isalpha()

def verificar_celular( celular ): #VALIDANDO TELEFONE, PARA QUE POSSUA MAIS DE 11 DIGITOS 
    """VERIFICA SE O CELULAR É VAIDO '(DDD)99999-9999'"""
    modelo = '[0-9]{2} [0-9]{5}-[0-9]{4}'
    resposta = re.findall( modelo, celular )
    return resposta
     