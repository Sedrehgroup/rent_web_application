# Generated by Django 4.1.3 on 2022-11-23 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_alter_user_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otpcode',
            name='phone_number',
            field=models.CharField(max_length=13, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(max_length=13, unique=True),
        ),
    ]
