# Generated by Django 2.2 on 2019-05-12 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('msgs', '0002_auto_20190512_1613'),
    ]

    operations = [
        migrations.AlterField(
            model_name='msgs',
            name='msg',
            field=models.CharField(max_length=200, verbose_name='消息'),
        ),
    ]