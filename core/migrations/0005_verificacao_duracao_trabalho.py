# Generated by Django 5.0.1 on 2024-01-27 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_remove_verificacao_horas_trabalhadas_horas_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='verificacao',
            name='duracao_trabalho',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
