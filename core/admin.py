from django.contrib import admin
from .models import Verificacao, Pessoa, Empresa



@admin.register(Pessoa)
class PessoaAdm(admin.ModelAdmin):
    list_display = ('nome', 'imagem', 'empresa',)

@admin.register(Verificacao)
class VerificacaoAdmin(admin.ModelAdmin):
    list_display = ('pessoa', 'horario', 'entrada_correta', 'saida_correta', 'duracao_trabalho','horario_entrada','horario_saida',)

  
@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'hora_entrada', 'hora_saida',)