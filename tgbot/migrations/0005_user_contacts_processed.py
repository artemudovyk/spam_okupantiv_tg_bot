# Generated by Django 3.2.12 on 2022-03-04 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tgbot', '0004_contact_telegramgroup'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='contacts_processed',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
