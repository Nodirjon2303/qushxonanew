# Generated by Django 4.0.4 on 2022-05-28 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0027_alter_client_id_alter_expenseclient_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incomeclient',
            name='weight',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]
