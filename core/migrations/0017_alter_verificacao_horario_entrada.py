# Generated by Django 5.0.1 on 2024-01-29 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_alter_verificacao_horario_entrada_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verificacao',
            name='horario_entrada',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]