from validate_docbr import CPF, CNPJ
from email_validator import validate_email,  EmailNotValidError, EmailSyntaxError
import re

def verificar_cpf( numero_cpf ): #VALIDANDO CPF, PARA QUE POSSUA 11 DIGITOS 
    cpf = CPF()
    return cpf.validate( numero_cpf )

def verificar_inscricao_estadual( inscricao_estadual ): #VALIDANDO RG, PARA QUE POSSUA 9 DIGITOS
    return len( inscricao_estadual ) == 9

def verificar_cnpj( numero_cnpj ): #VALIDANDO CPF, PARA QUE POSSUA 11 DIGITOS 
    cnpj = CNPJ()
    return cnpj.validate( numero_cnpj )

def verificar_rg( rg ): #VALIDANDO RG, PARA QUE POSSUA 9 DIGITOS
    return len( rg ) == 9

def verificar_nome( nome ): #VALIDANDO NOME, PARA QUE NÃO POSSUA NÚMEROS 
    return all(char.isalpha() or char.isspace() for char in nome)

def verificar_celular( celular ): #VALIDANDO TELEFONE, PARA QUE POSSUA MAIS DE 11 DIGITOS 
    """VERIFICA SE O CELULAR É VALIDO '(DDD)99999-9999'"""
    # modelo = '([0-9]{2}) [0-9]{5}-[0-9]{4}'
    modelo = r'\(\d{2}\) \d{5}-\d{4}'
    resposta = re.findall( modelo, celular )
    return resposta
    
def verificar_email( email ):
    """VERIFICA SE O EMAIL ESTÁ CORRETO E SE É VÁLIDO(SE EXISTE)"""
    try:
        validate_email( email )
    except EmailNotValidError as e:
        print(str(e))
        return False
    
    except Exception as e:
        print(str(e))
        return False
    
    return True