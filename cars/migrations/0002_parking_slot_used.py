# Generated by Django 2.0.7 on 2020-02-24 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='parking',
            name='slot_used',
            field=models.IntegerField(default=0),
        ),
    ]
