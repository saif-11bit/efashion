# Generated by Django 3.1.6 on 2021-04-08 03:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0032_auto_20210408_0847'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='thirty_four_size',
            field=models.BooleanField(null=True),
        ),
    ]