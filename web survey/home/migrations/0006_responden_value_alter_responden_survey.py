# Generated by Django 4.0.6 on 2022-08-13 16:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_responden_answer'),
    ]

    operations = [
        migrations.AddField(
            model_name='responden',
            name='value',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.surveyquestion'),
        ),
        migrations.AlterField(
            model_name='responden',
            name='Survey',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.survey'),
        ),
    ]