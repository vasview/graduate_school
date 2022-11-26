# Generated by Django 4.1.1 on 2022-11-21 19:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("postgraduates", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="postgraduate",
            name="student",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="students",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]