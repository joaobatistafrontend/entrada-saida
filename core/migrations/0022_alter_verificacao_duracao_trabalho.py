# Generated by Django 5.0.1 on 2024-01-29 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_alter_verificacao_duracao_trabalho'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verificacao',
            name='duracao_trabalho',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
