# Generated by Django 5.2.1 on 2025-06-04 12:09

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("login", "0012_endereco"),
    ]

    operations = [
        migrations.AddField(
            model_name="endereco",
            name="userEndereco",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="endereco",
            name="bairro",
            field=models.CharField(max_length=50),
        ),
    ]
