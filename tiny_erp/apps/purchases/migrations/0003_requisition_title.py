# pylint: disable=invalid-name,missing-docstring
# # Generated by Django 2.2.3 on 2019-07-16 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("purchases", "0002_auto_20190709_1952")]

    operations = [
        migrations.AddField(
            model_name="requisition",
            name="title",
            field=models.CharField(
                default="Purchase Requisition", max_length=255, verbose_name="Title"
            ),
            preserve_default=False,
        )
    ]
