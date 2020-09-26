# Generated by Django 3.1.1 on 2020-09-26 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_auto_20200925_2126'),
    ]

    operations = [
        migrations.CreateModel(
            name='SocketModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('socket_id', models.CharField(max_length=50)),
                ('seller_id', models.EmailField(max_length=254)),
            ],
        ),
        migrations.AlterModelOptions(
            name='callabacks',
            options={'verbose_name': 'Callback', 'verbose_name_plural': 'Callbacks'},
        ),
        migrations.AlterModelOptions(
            name='ordertrak',
            options={'verbose_name': 'Trak', 'verbose_name_plural': 'Trak Orders'},
        ),
        migrations.AlterModelOptions(
            name='status',
            options={'verbose_name': 'Status', 'verbose_name_plural': 'Status'},
        ),
    ]