# Generated by Django 2.2.6 on 2019-11-20 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lucky', '0003_auto_20191120_0926'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermaster',
            name='profile',
            field=models.FileField(blank=True, upload_to='profile'),
        ),
    ]