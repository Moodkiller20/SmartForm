# Generated by Django 4.1.7 on 2023-04-04 00:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smart_emailApp', '0012_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='link',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='link',
            name='updated_at',
            field=models.DateField(auto_now=True, null=True),
        ),
    ]
