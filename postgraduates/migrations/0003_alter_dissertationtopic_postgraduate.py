# Generated by Django 4.1.1 on 2022-11-23 06:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("postgraduates", "0002_alter_postgraduate_student"),
    ]

    operations = [
        migrations.AlterField(
            model_name="dissertationtopic",
            name="postgraduate",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="topics",
                to="postgraduates.postgraduate",
            ),
        ),
    ]