# Generated by Django 5.2.1 on 2025-05-10 11:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
        ('enrollment', '0001_initial'),
        ('instructors', '0001_initial'),
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Coueses',
            new_name='Courses',
        ),
    ]
