# Generated by Django 2.0 on 2020-03-31 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('df', '0002_person_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='Corren',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doll', models.FloatField()),
                ('euro', models.FloatField()),
            ],
        ),
    ]