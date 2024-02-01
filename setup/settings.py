from pathlib import Path, os
from dotenv import load_dotenv
load_dotenv()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = str( os.getenv('SECRET_KEY') )
#'django-insecure-$(hiv=nruy-%28(uww8tl@sl*$#4oeygal+z-*!n9rxj*mz9$g'
DEBUG = True

ALLOWED_HOSTS = ['192.168.31.105', 'localhost']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.gerador_proposta.apps.GeradorPropostaConfig',
    'apps.pessoas.apps.PessoasConfig',
    'apps.financeiros.apps.FinanceirosConfig',
    'rest_framework'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'setup.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'setup.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }
DATABASES = {
        'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'universo_futurjet',
        'USER': 'flavio',
        'PASSWORD': 'Futurjet@2023',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
        'charset': "utf8mb4",
        'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# VERSIONAMENTO 
# DEFINIDO PELA URL 'EX: 192.168.31.222:4000/v1/pessoas/clientes
DEFAULT_VERSIONING_SCHEME = 'url'

REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.QueryParameterVersioning',
    # 'DEFAULT_PERMISSION_CLASSES':[ #DEFININDO EM TODOS OS VIEWSET AS PERMISSÕES
    #     'rest_framework.permissions.IsAuthenticated',
    #     'rest_framework.permissions.DjangoModelPermissions'
    # ], #DEFININDO NO PROJETO QUE USARÁ O 'BASICAUTHENTICATION'
    # 'DEFAULT_AUTHENTICATION_CLASSES':[
    #     'rest_framework.authentication.BasicAuthentication'
    # ],
    #LIMITANDO ACESSO Á API
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle', #IMPORTAÇÃO PARA LIMITAR USUÁRIO ANÔNIMO
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day', #'anon'== 'Anônimo' |'5/day' Limite de 5 requisições por dia 
    },
}
