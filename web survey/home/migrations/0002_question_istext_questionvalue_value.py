# Generated by Django 4.0.6 on 2022-08-13 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='isText',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='questionvalue',
            name='value',
            field=models.IntegerField(blank=True, default=1),
            preserve_default=False,
        ),
    ]
