# Generated by Django 3.1.6 on 2021-03-16 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0021_emailnewsletter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='p_dis_price',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
