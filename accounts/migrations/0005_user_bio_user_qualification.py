# Generated by Django 5.0.3 on 2024-07-16 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_jobseeker_experience'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='bio',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='user',
            name='qualification',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
