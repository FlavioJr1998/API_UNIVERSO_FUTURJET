from django.contrib import admin
from apps.gerador_proposta.models import TBA_ItensUpgradeVersaoMaquina, TB_Item

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

class ListandoItem( admin.ModelAdmin):
    """
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
    """
    list_display = ( "id","descricao","preco_custo","upgrade","codigo_upgrade" )
    list_display_links = ( "id","descricao" )
    search_fields = ( "id","descricao" )
    
admin.site.register( TB_Item, ListandoItem )