# Generated by Django 3.1.1 on 2020-09-14 04:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ministers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='politic',
            name='minister_name',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
