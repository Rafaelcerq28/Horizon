# Generated by Django 2.1 on 2021-04-02 00:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0018_produtos_imagem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produtos',
            name='imagem',
            field=models.ImageField(blank=True, null=True, upload_to='media/images/'),
        ),
    ]
