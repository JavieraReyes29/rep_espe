# Generated by Django 2.0.2 on 2023-05-24 05:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ordencompra', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordencompra',
            name='proveedor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prov.Proveedor'),
        ),
    ]
