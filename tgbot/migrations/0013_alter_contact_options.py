# Generated by Django 3.2.12 on 2022-03-07 19:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tgbot', '0012_auto_20220305_2238'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contact',
            options={'ordering': ['repeats', 'failed_repeats']},
        ),
    ]
