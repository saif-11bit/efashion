# Generated by Django 3.1.6 on 2021-02-18 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_merge_20210218_1322'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='second_img',
            field=models.ImageField(null=True, upload_to='Second Img'),
        ),
        migrations.AddField(
            model_name='item',
            name='third_img',
            field=models.ImageField(null=True, upload_to='Third Img'),
        ),
        migrations.AlterField(
            model_name='review',
            name='desc',
            field=models.CharField(max_length=300),
        ),
    ]
