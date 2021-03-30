# Generated by Django 3.1.7 on 2021-03-12 06:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20210312_0852'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(default='', max_length=255)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('event', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='event_user', to='api.userregisterevent')),
            ],
            options={
                'ordering': ['event'],
            },
        ),
    ]