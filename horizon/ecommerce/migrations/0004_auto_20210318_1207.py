# Generated by Django 2.1 on 2021-03-18 15:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0003_auto_20210318_1205'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='produtos',
            name='categoria',
        ),
        migrations.DeleteModel(
            name='Categorias',
        ),
    ]