# Generated by Django 4.2.20 on 2025-05-06 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0003_pedido'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='categoria',
            field=models.CharField(default='Sem Categoria', max_length=50),
        ),
    ]
