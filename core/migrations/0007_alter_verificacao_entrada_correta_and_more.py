# Generated by Django 5.0.1 on 2024-01-27 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_alter_verificacao_entrada_correta_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verificacao',
            name='entrada_correta',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='verificacao',
            name='saida_correta',
            field=models.BooleanField(default=False),
        ),
    ]