from django.contrib import admin
from apps.pessoas.models import *

class ListandoClientes( admin.ModelAdmin):
    list_display = ("id","nome", "get_tipo_pessoa","get_endereco","get_cidade")
    list_display_links = ("id", "nome")
    search_fields = ("id","nome")

    def get_tipo_pessoa( self, obj ):
        return f"{obj.tipo_pessoa.descricao}"
    def get_endereco( self, obj ):
        return f"{obj.endereco.rua},{obj.endereco.numero}-{obj.endereco.bairro}"
    def get_cidade( self, obj):
        return f"{obj.endereco.cidade}-{obj.endereco.estado}"
admin.site.register( Cliente, ListandoClientes )

