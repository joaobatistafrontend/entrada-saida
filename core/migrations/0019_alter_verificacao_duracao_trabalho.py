# Generated by Django 5.0.1 on 2024-01-29 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_alter_verificacao_horario_entrada'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verificacao',
            name='duracao_trabalho',
            field=models.DurationField(blank=True, null=True),
        ),
    ]
