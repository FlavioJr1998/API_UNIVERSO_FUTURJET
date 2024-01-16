import os, django
from faker import Faker
from validate_docbr import CPF, CNPJ
import random
from apps.pessoas.models import *

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()



def criando_financeiros(quantidade):
    fake = Faker('pt_BR')
    Faker.seed(10)
    for _ in range(quantidade):
        pass

criando_financeiros(50)
print('Sucesso!')