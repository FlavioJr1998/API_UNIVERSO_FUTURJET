from rest_framework import routers
from django.contrib import admin
from django.urls import path, include
from apps.pessoas.views import ClientesViewSet 
from apps.gerador_proposta.views import PropostasViewSet

router = routers.DefaultRouter()
router.register('pessoas/clientes', ClientesViewSet )
router.register('gerador_proposta', PropostasViewSet )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]
