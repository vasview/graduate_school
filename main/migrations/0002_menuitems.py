# Generated by Django 4.1.1 on 2022-11-26 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="MenuItems",
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
                ("title", models.CharField(max_length=50)),
                ("url_name", models.CharField(max_length=250)),
                ("sort", models.SmallIntegerField()),
                (
                    "seen_by",
                    models.IntegerField(
                        choices=[
                            (1, "аспирант"),
                            (2, "руководитель"),
                            (3, "администрация"),
                        ],
                        default=1,
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={
                "verbose_name": "",
                "verbose_name_plural": "",
                "ordering": ["sort"],
            },
        ),
    ]