# Generated by Django 3.1.7 on 2021-04-26 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_userevent_is_approved'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventhistory',
            name='image',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]