# Generated by Django 4.2.4 on 2023-12-15 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('box', '0003_remove_item_uuid_itemportion_uuid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='barcode',
        ),
        migrations.AddField(
            model_name='itemportion',
            name='barcode',
            field=models.ImageField(blank=True, default='C:\\Users\\Eddie Tang\\PythonProjects\\djangobox\\djangobox\\media\\barcodes\\barcode.png', upload_to='C:\\Users\\Eddie Tang\\PythonProjects\\djangobox\\djangobox\\media\\barcodes'),
        ),
    ]
