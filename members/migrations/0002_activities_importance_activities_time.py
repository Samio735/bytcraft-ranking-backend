# Generated by Django 4.2.4 on 2023-08-29 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='activities',
            name='importance',
            field=models.CharField(choices=[('training', 'Training'), ('important', 'Important')], default='training', max_length=100),
        ),
        migrations.AddField(
            model_name='activities',
            name='time',
            field=models.CharField(choices=[('quick', 'Quick'), ('takes-time', 'Takes time'), ('ongoin', 'Ongoin')], default='quick', max_length=100),
        ),
    ]
