# Generated by Django 5.0.1 on 2024-01-27 17:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_verificacao_horas_trabalhadas_horas_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='verificacao',
            name='horas_trabalhadas_horas',
        ),
        migrations.RemoveField(
            model_name='verificacao',
            name='horas_trabalhadas_minutos',
        ),
        migrations.DeleteModel(
            name='RegistroHoras',
        ),
    ]
