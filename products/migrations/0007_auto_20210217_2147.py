# Generated by Django 3.1.6 on 2021-02-17 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_review'),
    ]

    operations = [
        migrations.CreateModel(
            name='Available_For',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
            ],
        ),
        migrations.RemoveField(
            model_name='category',
            name='_for',
        ),
    ]
