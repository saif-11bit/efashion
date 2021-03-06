# Generated by Django 3.1.6 on 2021-02-20 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0015_auto_20210220_1311'),
    ]

    operations = [
        migrations.RenameField(
            model_name='address',
            old_name='address_line2',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='address',
            name='default',
        ),
        migrations.AddField(
            model_name='address',
            name='phone_n',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='city',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='pin_code',
            field=models.CharField(max_length=6, null=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='state',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='street_address',
            field=models.CharField(max_length=200, null=True),
        ),
    ]