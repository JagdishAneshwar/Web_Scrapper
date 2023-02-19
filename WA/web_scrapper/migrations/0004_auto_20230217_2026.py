# Generated by Django 3.2.16 on 2023-02-17 14:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('web_scrapper', '0003_auto_20230127_2353'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='url',
        ),
        migrations.RemoveField(
            model_name='urls',
            name='user',
        ),
        migrations.AddField(
            model_name='tag',
            name='tags',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='web_scrapper.urls'),
        ),
        migrations.AddField(
            model_name='urls',
            name='urls',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
