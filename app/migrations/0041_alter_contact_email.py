# Generated by Django 5.2 on 2025-05-08 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0040_delete_mymodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='email',
            field=models.EmailField(max_length=30),
        ),
    ]
