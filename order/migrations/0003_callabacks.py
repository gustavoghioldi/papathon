# Generated by Django 3.1.1 on 2020-09-25 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_auto_20200925_1848'),
    ]

    operations = [
        migrations.CreateModel(
            name='callabacks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url_callback', models.URLField()),
                ('api_key', models.CharField(max_length=50)),
            ],
        ),
    ]