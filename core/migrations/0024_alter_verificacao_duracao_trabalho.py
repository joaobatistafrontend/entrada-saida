# Generated by Django 5.0.1 on 2024-01-29 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_alter_verificacao_duracao_trabalho'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verificacao',
            name='duracao_trabalho',
            field=models.TimeField(blank=True, null=True),
        ),
    ]