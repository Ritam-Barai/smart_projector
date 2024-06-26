# Generated by Django 5.0.6 on 2024-06-15 05:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdfs', '0003_remove_pdf_session'),
        ('sessions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pdf',
            name='session',
            field=models.ForeignKey(default='default', on_delete=django.db.models.deletion.CASCADE, to='sessions.session'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pdf',
            name='some_field',
            field=models.CharField(default='default_value', max_length=200),
        ),
    ]
