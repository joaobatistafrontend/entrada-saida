from django.contrib import admin
from .models import Verificacao, Pessoa, Empresa



@admin.register(Pessoa)
class PessoaAdm(admin.ModelAdmin):
    list_display = ('nome', 'imagem', 'empresa',)

@admin.register(Verificacao)
class VerificacaoAdmin(admin.ModelAdmin):
    list_display = ('pessoa', 'horario', 'entrada_correta', 'saida_correta', 'duracao_trabalho')

    def calcular_duracao_display(self, obj):
        horas, minutos = obj.calcular_duracao()
        return f"{horas}h {minutos}min"

    calcular_duracao_display.short_description = 'Duração'
    search_fields = ('pessoa__nome',)  # Adicione isso se quiser poder pesquisar pelo nome da pessoa

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'hora_entrada', 'hora_saida',)