# Generated by Django 2.0 on 2018-01-25 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_productincart_session_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='productincart',
            name='size',
            field=models.IntegerField(default=30, verbose_name='Размер пиццы(диаметр в см)'),
        ),
    ]
