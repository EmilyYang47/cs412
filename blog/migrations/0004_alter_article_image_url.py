# Generated by Django 5.2.1 on 2025-06-03 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='image_url',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]
