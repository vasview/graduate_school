# Generated by Django 4.1.1 on 2023-01-14 20:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AcademicDegree',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=50, null=True)),
                ('name', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'Ученая степень',
                'verbose_name_plural': 'Справочник ученых степеней',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='AcademicTitle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'Звание преподавателя',
                'verbose_name_plural': 'Справочник званий преподавателей',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=50, null=True)),
                ('name', models.CharField(max_length=200)),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Кафедра',
                'verbose_name_plural': 'Список кафедр',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=50, null=True)),
                ('name', models.CharField(max_length=200)),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Факультет',
                'verbose_name_plural': 'Список факультетов',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Specialty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=50, null=True)),
                ('name', models.CharField(max_length=200)),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Специальность',
                'verbose_name_plural': 'Справочник специальностей',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=50, null=True)),
                ('name', models.CharField(max_length=200)),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Дисциплина',
                'verbose_name_plural': 'Справочник дисциплин',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Supervisor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('academic_degree', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='faculties.academicdegree')),
                ('academic_title', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='faculties.academictitle')),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='faculties.department')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Научный руководитель',
                'verbose_name_plural': 'Научные руководители',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=150, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Администрация - представитель',
                'verbose_name_plural': 'Администрация - представители',
                'ordering': ['id'],
            },
        ),
        migrations.AddField(
            model_name='department',
            name='faculty',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='faculties.faculty'),
        ),
    ]
