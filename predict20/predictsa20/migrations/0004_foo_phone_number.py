# Generated by Django 4.2.9 on 2024-01-23 14:20

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ("predictsa20", "0003_foo"),
    ]

    operations = [
        migrations.AddField(
            model_name="foo",
            name="phone_number",
            field=phonenumber_field.modelfields.PhoneNumberField(
                blank=True, max_length=128, region=None
            ),
        ),
    ]
