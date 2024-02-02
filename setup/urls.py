from rest_framework import routers
from django.contrib import admin
from django.urls import path, include, register_converter
from apps.pessoas.views import ClientesViewSet 
from apps.gerador_proposta.views import PropostasViewSet, ModeloMaquinaViewSet, VersaoMaquinaViewSet, ItemViewSet

class BoolConverter:
    #Conversor 'bool', pois o django não possui nativo
     
    regex = r'true|false' #Definindo os valores que a classe vai aceitar

    def to_python(self, value): #Convertendo para o python conseguir manipular
        return value.lower() == 'true'

    def to_url(self, value): #Convertendo novamente para 'url'
        return 'true' if value else 'false'

register_converter(BoolConverter, 'bool') #Informando para o django a conversão


router = routers.DefaultRouter()
router.register('pessoas/clientes', ClientesViewSet )
router.register('gerador_proposta', PropostasViewSet )
router.register('modelo', ModeloMaquinaViewSet )
router.register('versao', VersaoMaquinaViewSet )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('modelo/<int:modelo_id>/versoes/', ModeloMaquinaViewSet.obter_versoes_por_modelo, name='obter_versoes_por_modelo'),
    path('item/upgrade/bool/<bool:bool_upgrade>/', ItemViewSet.obter_itens_upgrade, name='obter_itens_upgrade'),
]


