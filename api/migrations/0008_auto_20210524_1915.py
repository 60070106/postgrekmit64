# Generated by Django 3.1.7 on 2021-05-24 12:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_eventhistory_image'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='eventhistory',
            options={'ordering': ['time']},
        ),
    ]
