# Generated by Django 4.0.3 on 2022-04-05 02:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0006_alter_user_profile_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='coins',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
