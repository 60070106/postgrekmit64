# Generated by Django 3.1.7 on 2021-03-30 07:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organizer', models.CharField(max_length=255)),
                ('location', models.TextField()),
                ('duration', models.TextField()),
                ('event_name', models.CharField(default='', max_length=255, unique=True)),
                ('event_image', models.TextField()),
                ('detail', models.TextField()),
                ('is_check', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['organizer'],
            },
        ),
        migrations.RemoveField(
            model_name='user',
            name='birth_date',
        ),
        migrations.RemoveField(
            model_name='user',
            name='location',
        ),
        migrations.AddField(
            model_name='user',
            name='is_approver',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='is_camper',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='is_organizer',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='phone',
            field=models.CharField(default='', max_length=12),
        ),
        migrations.CreateModel(
            name='UserRegisterEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='register_user', to='api.userevent')),
                ('user', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['event'],
            },
        ),
        migrations.CreateModel(
            name='UserImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imgpath', models.TextField()),
                ('user', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='image', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['user'],
            },
        ),
        migrations.AddField(
            model_name='userevent',
            name='appoved_by',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='approver_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='userevent',
            name='user',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='event', to=settings.AUTH_USER_MODEL),
        ),
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
        migrations.CreateModel(
            name='EventDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.TextField()),
                ('event', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='event_document', to='api.userevent')),
            ],
            options={
                'ordering': [],
            },
        ),
        migrations.CreateModel(
            name='EventAppovedLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('agreed', models.BooleanField(default=False)),
                ('detail', models.TextField()),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('event', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='event', to='api.userevent')),
                ('user', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='approver', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['event'],
            },
        ),
    ]
