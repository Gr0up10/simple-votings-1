# Generated by Django 3.0.1 on 2020-01-25 16:28

import datetime
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
            name='Voting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=500)),
                ('image', models.ImageField(null=True, upload_to='')),
                ('create_date', models.DateTimeField(default=datetime.datetime.now)),
                ('vtype', models.PositiveSmallIntegerField(choices=[(1, 'Дискретный выбор'), (2, 'Один из многих'), (3, 'Несколько из многих')], default=1)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='VoteVariant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('voting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Voting')),
            ],
        ),
        migrations.CreateModel(
            name='VoteFact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=datetime.datetime.now)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('variant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.VoteVariant')),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=2000)),
                ('vtype', models.PositiveSmallIntegerField(choices=[(0, 'Отправлено модераторам'), (1, 'На рассмотрении'), (2, 'Вердикт положительный'), (3, 'Вердикт отрицательный')], default=1)),
                ('comment', models.CharField(max_length=200, null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('vote', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Voting')),
            ],
        ),
    ]
