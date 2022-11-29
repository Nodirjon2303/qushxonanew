# Generated by Django 4.1.3 on 2022-11-30 03:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0038_alter_expensesotuvchi_amount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incomeclient',
            name='product_dehqon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='incomeclients', to='app.expensedehqon', verbose_name='Dehqonning mahsuloti'),
        ),
        migrations.AlterField(
            model_name='incomesotuvchi',
            name='source',
            field=models.CharField(choices=[('bozor', 'Bozor'), ('qushxona', 'Qushxona')], default='qushxona', max_length=125, verbose_name='Manba'),
        ),
    ]
