# Generated by Django 2.2 on 2019-05-02 22:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0003_auto_20190502_2155'),
    ]

    operations = [
        migrations.CreateModel(
            name='Msgs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('send_time', models.DateTimeField(auto_now_add=True, verbose_name='发送时间')),
                ('msg', models.CharField(max_length=200, verbose_name='消息')),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='msgs_receiver', to='users.User', verbose_name='接收者')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='msgs_sender', to='users.User', verbose_name='发送者')),
            ],
        ),
    ]
