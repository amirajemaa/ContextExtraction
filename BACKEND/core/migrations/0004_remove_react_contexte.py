# Generated by Django 3.2.2 on 2021-05-28 12:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_react_contexte'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='react',
            name='contexte',
        ),
    ]
