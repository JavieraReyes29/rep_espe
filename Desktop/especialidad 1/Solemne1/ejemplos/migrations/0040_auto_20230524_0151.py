# Generated by Django 2.0.2 on 2023-05-24 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ordencompra', '0002_auto_20230524_0151'),
        ('ejemplos', '0039_auto_20230524_0124'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Proveedor',
        ),
        migrations.AlterField(
            model_name='producto',
            name='proveedor',
            field=models.ManyToManyField(to='prov.Proveedor'),
        ),
    ]