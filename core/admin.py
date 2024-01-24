from django.contrib import admin
from .models import Verificacao, Pessoa, Empresa



@admin.register(Pessoa)
class PessoaAdm(admin.ModelAdmin):
    list_display = ('nome', 'imagem', 'empresa',)

@admin.register(Verificacao)
class VerificacaoAdmin(admin.ModelAdmin):
    list_display = ('pessoa', 'horario', 'obter_status_saida', 'entrada_correta', 'saida_correta')
    search_fields = ('pessoa__nome',)  # Adicione isso se quiser poder pesquisar pelo nome da pessoa

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'hora_entrada', 'hora_saida',)