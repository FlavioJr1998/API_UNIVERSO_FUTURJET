from rest_framework import routers
from django.contrib import admin
from django.urls import path, include
from apps.pessoas.views import ClientesViewSet 
from apps.gerador_proposta.views import PropostasViewSet, ModeloMaquinaViewSet, VersaoMaquinaViewSet, ItemSerializer

router = routers.DefaultRouter()
router.register('pessoas/clientes', ClientesViewSet )
router.register('gerador_proposta', PropostasViewSet )
router.register('modelo', ModeloMaquinaViewSet )
router.register('versao', VersaoMaquinaViewSet )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('modelo/<int:modelo_id>/versoes/', ModeloMaquinaViewSet.obter_versoes_por_modelo, name='obter_versoes_por_modelo'),
    # path('item/upgrade/bool/<boolean:bool_upgrade>', ItemSerializer.obter_versoes_por_modelo, name='obter_versoes_por_modelo'),
]
