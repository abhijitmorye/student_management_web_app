# Generated by Django 3.2.2 on 2021-12-06 03:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_management_app', '0003_alter_leavereportstudent_leave_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leavereportstaffs',
            name='leave_status',
            field=models.IntegerField(default=0),
        ),
    ]
