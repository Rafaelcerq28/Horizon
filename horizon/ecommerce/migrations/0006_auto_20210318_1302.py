# Generated by Django 2.1 on 2021-03-18 16:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0005_auto_20210318_1209'),
    ]

    operations = [
        migrations.CreateModel(
            name='Carrinho',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Clientes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
                ('endereço', models.CharField(max_length=255)),
                ('complemento', models.CharField(max_length=255)),
                ('cep', models.CharField(max_length=8)),
                ('telefone', models.CharField(max_length=11)),
                ('cpf', models.CharField(max_length=11)),
                ('rg', models.CharField(max_length=9)),
                ('sexo', models.CharField(choices=[('m', 'M'), ('m', 'F'), ('outros', 'Outros')], max_length=1)),
                ('idade', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='carrinho',
            name='cliente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerce.Clientes'),
        ),
        migrations.AddField(
            model_name='carrinho',
            name='produto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerce.Produtos'),
        ),
    ]
