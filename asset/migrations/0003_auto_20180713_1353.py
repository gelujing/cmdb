# Generated by Django 2.0.4 on 2018-07-13 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asset', '0002_auto_20180713_1211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assetloginuser',
            name='private_key',
            field=models.FileField(blank=True, null=True, upload_to='upload/privatekey/%Y%m%d28970', verbose_name='私钥'),
        ),
    ]
