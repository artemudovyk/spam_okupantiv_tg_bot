# Generated by Django 3.2.12 on 2022-03-05 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tgbot', '0010_alter_contact_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contact',
            name='proccessed_by',
        ),
        migrations.AddField(
            model_name='user',
            name='contacts_processed_num',
            field=models.PositiveIntegerField(default=0, editable=False),
        ),
        migrations.RemoveField(
            model_name='user',
            name='contacts_processed',
        ),
        migrations.AddField(
            model_name='user',
            name='contacts_processed',
            field=models.ManyToManyField(to='tgbot.Contact'),
        ),
    ]
