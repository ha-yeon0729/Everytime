# Generated by Django 3.2.10 on 2021-12-28 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0012_auto_20211228_2032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='ssgPw',
            field=models.CharField(max_length=200),
        ),
    ]
