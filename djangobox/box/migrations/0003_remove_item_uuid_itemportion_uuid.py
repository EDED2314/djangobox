# Generated by Django 4.2.4 on 2023-12-15 21:25

from django.db import migrations
import shortuuidfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('box', '0002_alter_box_boxes_alter_item_unit'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='uuid',
        ),
        migrations.AddField(
            model_name='itemportion',
            name='uuid',
            field=shortuuidfield.fields.ShortUUIDField(blank=True, editable=False, max_length=22),
        ),
    ]