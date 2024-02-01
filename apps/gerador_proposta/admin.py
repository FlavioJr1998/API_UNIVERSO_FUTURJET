from django.contrib import admin
from apps.gerador_proposta.models import TBA_ItensUpgradeVersaoMaquina

class ListandoItensUpgrade( admin.ModelAdmin):
    list_display = ( "get_proposta","get_item" )
    list_display_links = ( "get_proposta","get_item" )
    search_fields = ( "get_proposta","get_item" )
  
    def get_proposta( self, instance ):
        descricao = f"|{instance.proposta.id}|{instance.proposta.cliente.nome}|{instance.proposta.versao_maquina.modelo.descricao}|{instance.proposta.versao_maquina.descricao}|"
        return descricao
    
    def get_item( self, instance ):
        return instance.item
    
admin.site.register( TBA_ItensUpgradeVersaoMaquina, ListandoItensUpgrade )