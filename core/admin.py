from django.contrib import admin
from .models import Vendedor, Produto

admin.site.register(Produto)

@admin.register(Vendedor)
class VendedorAdmin(admin.ModelAdmin):
    list_display  = ['nome', 'telefone', 'email', 'cpf', 'cadastro']
    search_fields = ['nome', 'cpf', 'email']
    readonly_fields = ['cadastro']