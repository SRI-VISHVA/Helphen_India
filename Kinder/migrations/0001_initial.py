# Generated by Django 3.0.4 on 2020-03-31 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=52)),
                ('email_id', models.EmailField(max_length=254)),
                ('message', models.TextField()),
            ],
        ),
    ]