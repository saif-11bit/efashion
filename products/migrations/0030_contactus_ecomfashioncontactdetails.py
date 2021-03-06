# Generated by Django 3.1.6 on 2021-04-02 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0029_about'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactUs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('phone_num', models.CharField(max_length=11)),
                ('message', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='EcomfashionContactDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.TextField()),
                ('phone_num', models.CharField(max_length=50)),
                ('gmail', models.CharField(max_length=50)),
            ],
        ),
    ]
