# Generated by Django 3.2.12 on 2022-03-04 23:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tgbot', '0006_alter_user_contacts_processed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contact',
            name='source_group',
        ),
    ]