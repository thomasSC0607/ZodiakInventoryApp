# Generated by Django 5.2 on 2025-05-11 16:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app1", "0004_cliente_zapato_pedido"),
    ]

    operations = [
        migrations.AddField(
            model_name="zapato",
            name="estado",
            field=models.CharField(
                choices=[
                    ("P", "Pendiente"),
                    ("PR", "En Producción"),
                    ("A", "Anulado"),
                    ("C", "Completado"),
                    ("E", "Entregado"),
                    ("B", "En Bodega"),
                ],
                default="P",
                max_length=2,
            ),
        ),
    ]
