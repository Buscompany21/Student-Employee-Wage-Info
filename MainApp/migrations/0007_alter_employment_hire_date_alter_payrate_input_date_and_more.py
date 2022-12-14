# Generated by Django 4.1.2 on 2022-10-28 06:41

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('MainApp', '0006_payrate_input_date_alter_employment_hire_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employment',
            name='hire_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='payrate',
            name='input_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='person',
            name='email',
            field=models.EmailField(max_length=254),
        ),
    ]
