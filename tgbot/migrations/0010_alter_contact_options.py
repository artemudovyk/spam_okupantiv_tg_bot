# Generated by Django 3.2.12 on 2022-03-05 15:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tgbot', '0009_auto_20220305_1541'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contact',
            options={'ordering': ['-failed_repeats', 'repeats']},
        ),
    ]
