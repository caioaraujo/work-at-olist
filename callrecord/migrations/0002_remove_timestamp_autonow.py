# Generated by Django 2.2.3 on 2019-07-10 22:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('callrecord', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='callrecord',
            name='timestamp',
            field=models.DateTimeField(),
        ),
    ]
