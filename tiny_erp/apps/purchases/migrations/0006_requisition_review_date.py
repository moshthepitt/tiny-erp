# Generated by Django 3.0.7 on 2020-09-04 18:50
# pylint: disable=invalid-name,missing-docstring
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("purchases", "0005_remove_requisition_comments"),
    ]

    operations = [
        migrations.AddField(
            model_name="requisition",
            name="review_date",
            field=models.DateTimeField(
                blank=True, default=None, null=True, verbose_name="Review Date"
            ),
        ),
    ]
