# Generated by Django 5.2.1 on 2025-06-19 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0010_category_course_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True, unique=True)),
            ],
        ),
        migrations.RenameField(
            model_name='course',
            old_name='categorypyth',
            new_name='category',
        ),
    ]
