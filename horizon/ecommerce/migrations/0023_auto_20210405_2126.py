# Generated by Django 2.1 on 2021-04-06 00:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0022_auto_20210405_2110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produtos',
            name='percentual_desconto',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]