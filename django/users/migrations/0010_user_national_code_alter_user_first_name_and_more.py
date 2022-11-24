# Generated by Django 4.1.3 on 2022-11-23 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_useradditionalinformation_remove_user_is_admin_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='national_code',
            field=models.CharField(default='1122334455', max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(max_length=100),
        ),
    ]