# Generated by Django 4.2.7 on 2023-12-04 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_property_image_unit_tenant'),
    ]

    operations = [
        migrations.AddField(
            model_name='unit',
            name='name',
            field=models.CharField(blank=True, default='flat', max_length=100, null=True),
        ),
    ]