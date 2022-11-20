# Generated by Django 4.1.1 on 2022-11-20 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ApplicationParameters",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("code", models.CharField(max_length=100, unique=True)),
                ("name", models.CharField(max_length=250)),
                ("value", models.CharField(max_length=250)),
            ],
            options={
                "verbose_name": "Параметр приложения",
                "verbose_name_plural": "Параметры приложения",
                "ordering": ["id"],
            },
        ),
    ]
