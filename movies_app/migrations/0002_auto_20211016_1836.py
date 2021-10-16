# Generated by Django 3.2.8 on 2021-10-16 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customer',
            options={'ordering': ['first_name', 'last_name']},
        ),
        migrations.AlterModelOptions(
            name='genre',
            options={'ordering': ['title']},
        ),
        migrations.AlterField(
            model_name='film',
            name='description',
            field=models.TextField(null=True),
        ),
    ]