# Generated by Django 4.1 on 2023-04-03 10:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("web_scrapper", "0008_rename_attribute_navurls_navattribute_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="navurls",
            old_name="navuser",
            new_name="user",
        ),
    ]
