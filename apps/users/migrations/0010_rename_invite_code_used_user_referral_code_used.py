# Generated by Django 5.1.2 on 2024-11-02 11:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_remove_userreferralcode_is_used_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='invite_code_used',
            new_name='referral_code_used',
        ),
    ]
