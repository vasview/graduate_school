# Generated by Django 4.1.1 on 2022-11-27 19:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("profiles", "0003_alter_educationaldocument_user"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="country",
            options={
                "ordering": ["name"],
                "verbose_name": "Страна",
                "verbose_name_plural": "Справочник стран",
            },
        ),
    ]
