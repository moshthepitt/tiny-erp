# Generated by Django 3.0.7 on 2020-09-04 18:46
# pylint: disable=invalid-name,missing-docstring
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("purchases", "0004_auto_20200904_2142"),
    ]

    operations = [
        migrations.RemoveField(model_name="requisition", name="comments",),
    ]
