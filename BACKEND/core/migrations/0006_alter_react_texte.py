# Generated by Django 3.2.2 on 2021-05-29 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_react_contexte'),
    ]

    operations = [
        migrations.AlterField(
            model_name='react',
            name='texte',
            field=models.TextField(blank=True),
        ),
    ]
