# Generated by Django 3.0.5 on 2020-07-02 07:01

import attendance_sys.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance_sys', '0016_auto_20200702_1228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to=attendance_sys.models.student_directory_path),
        ),
    ]
