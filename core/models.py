from django.db import models
import datetime
from django.utils import timezone




class Verificacao(models.Model):
    pessoa = models.ForeignKey('Pessoa', on_delete=models.CASCADE)
    horario = models.DateTimeField(auto_now_add=True)
    
    horario_entrada = models.DateTimeField(blank=True, null=True)
    horario_saida = models.DateTimeField(blank=True, null=True)
    
    entrada_correta = models.BooleanField(default=False)
    saida_correta = models.BooleanField(default=False)
    duracao_trabalho = models.IntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # Calcula a duração de trabalho antes de salvar
        if self.horario_entrada and self.horario_saida:
            diff_minutes = (self.horario_saida - self.horario_entrada).total_seconds() / 60
            self.duracao_trabalho_minutos = int(diff_minutes)

    def obter_status_saida(self):
        return 'Saída' if self.saida_correta else 'Entrada'
class Empresa(models.Model):
    nome = models.CharField(max_length=100)
    hora_entrada = models.TimeField()
    hora_saida = models.TimeField()

    def __str__(self):
        return self.nome

class Pessoa(models.Model):
    nome = models.CharField(max_length=100)
    imagem = models.ImageField(upload_to='imagens/')

    # Relacionamento com a empresa
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome
    def registrar_verificacao(self, tipo_verificacao):
        agora = datetime.datetime.now().time()

        # Verifica se o tipo de verificação é válido ('entrada' ou 'saida')
        if tipo_verificacao not in ['entrada', 'saida']:
            raise ValueError("Tipo de verificação inválido. Use 'entrada' ou 'saida'.")

        # Verifica se a pessoa está no horário correto para registrar a entrada ou saída
        if tipo_verificacao == 'entrada' and self.verificar_horario_entrada():
            Verificacao.objects.create(pessoa=self, entrada_correta=True)
        elif tipo_verificacao == 'saida' and self.verificar_horario_saida():
            Verificacao.objects.create(pessoa=self, saida_correta=True)
        else:
            raise ValueError("A pessoa não está no horário correto para registrar a {}.".format(tipo_verificacao))



    def verificar_horario_entrada(self):
        agora = datetime.datetime.now().time()
        # Verifica se o horário atual está dentro do horário de entrada permitido pela empresa
        return agora >= self.empresa.hora_entrada

    def verificar_horario_saida(self):
        agora = datetime.datetime.now().time()
        # Verifica se o horário atual está dentro do horário de saída permitido pela empresa
        return agora <= self.empresa.hora_saida

    def calcular_horas_extras(self):
        # Calcula as horas extras apenas se a pessoa já tiver saído e tiver ultrapassado o horário de saída permitido
        if self.hora_saida and self.hora_saida > self.empresa.hora_saida:
            horas_trabalhadas = (self.hora_saida - self.empresa.hora_saida).seconds / 3600
            horas_normais = 9  # Quantidade de horas padrão
            horas_extras = max(horas_trabalhadas - horas_normais, 0)
            return horas_extras
        return 0



'''    def calcular_duracao(self):
        if self.horario_entrada and self.horario_saida:
            duracao = self.horario_entrada - self.horario
            duracao_em_minutos = int(duracao)
            return duracao_em_minutos
        else:
            return int(0)

    def save(self, *args, **kwargs):
        self.duracao_trabalho = self.calcular_duracao()
        super(Verificacao, self).save(*args, **kwargs)
'''