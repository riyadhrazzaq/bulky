# Generated by Django 3.1.1 on 2020-09-26 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender', models.EmailField(max_length=254, verbose_name='From')),
                ('subject', models.CharField(max_length=75, verbose_name='Subject')),
                ('content_plain', models.TextField()),
            ],
        ),
    ]