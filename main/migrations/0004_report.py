# Generated by Django 3.0.1 on 2020-01-14 13:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0003_votefact'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=2000)),
                ('vtype', models.PositiveSmallIntegerField(
                    choices=[(0, 'Отправлено модераторам'), (1, 'На рассмотрении'), (2, 'Вердикт положительный'),
                             (3, 'Вердикт отрицательный')], default=1)),
                ('comment', models.CharField(max_length=200, null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('vote', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Voting')),
            ],
        ),
    ]
