# Generated by Django 3.2.7 on 2022-01-25 12:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("mainapp", "0002_auto_20211223_1129"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="product",
            options={"ordering": ("-price", "name")},
        ),
    ]
