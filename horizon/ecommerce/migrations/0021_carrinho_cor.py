# Generated by Django 2.1 on 2021-04-05 19:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0020_auto_20210401_2152'),
    ]

    operations = [
        migrations.AddField(
            model_name='carrinho',
            name='cor',
            field=models.ForeignKey(default=14, on_delete=django.db.models.deletion.CASCADE, to='ecommerce.Cores'),
            preserve_default=False,
        ),
    ]