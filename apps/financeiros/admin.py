from django.contrib import admin
from apps.financeiros.models import *

class ListandoFormasPagamento( admin.ModelAdmin):
    list_display = ("id","descricao")
    list_display_links = ("id", "descricao")
    search_fields = ("id","descricao")
admin.site.register( FormaPagmento, ListandoFormasPagamento )
