# Generated by Django 3.1.6 on 2021-02-18 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_auto_20210218_1915'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='second_img',
            field=models.ImageField(blank=True, null=True, upload_to='Second Img'),
        ),
        migrations.AlterField(
            model_name='item',
            name='third_img',
            field=models.ImageField(blank=True, null=True, upload_to='Third Img'),
        ),
    ]
