# Generated by Django 5.0.3 on 2024-07-17 15:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_address'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Address',
        ),
    ]
