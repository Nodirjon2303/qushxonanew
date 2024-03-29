# Generated by Django 4.0.2 on 2022-11-13 13:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0031_alter_client_options_alter_expenseclient_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='expenseclient',
            options={'verbose_name': "Klient to'lovi", 'verbose_name_plural': "Klientlar to'lovlari"},
        ),
        migrations.AlterModelOptions(
            name='expensedehqon',
            options={'verbose_name': 'Dehqonlardan kelgan mol', 'verbose_name_plural': 'Dehqonlarning kelgan mollar'},
        ),
        migrations.AlterModelOptions(
            name='expensesotuvchi',
            options={'verbose_name': "Bozor sotuvchilari to'lovi", 'verbose_name_plural': "Bozor sotuvchilari to'lovlari"},
        ),
        migrations.AlterModelOptions(
            name='incomeclient',
            options={'verbose_name': 'Qushxona klienti sotib olgan mahsuloti', 'verbose_name_plural': 'Qushxona klienti sotib olgan mahsulolari'},
        ),
        migrations.AlterModelOptions(
            name='incomedehqon',
            options={'verbose_name': "Dehqonga to'langan pullar", 'verbose_name_plural': "Dehqonlarga to'langan pullar"},
        ),
        migrations.AlterModelOptions(
            name='incomesotuvchi',
            options={'verbose_name': 'Bozor sotuvchi sotib olgan mahsuloti', 'verbose_name_plural': 'Bozor sotuvchilari sotib olgan mahsulolari'},
        ),
        migrations.AlterModelOptions(
            name='xarajat',
            options={'verbose_name': 'Boshqa Xarajat', 'verbose_name_plural': 'Boshqa Xarajatlar'},
        ),
        migrations.AlterField(
            model_name='expensedehqon',
            name='price',
            field=models.BigIntegerField(blank=True, default=0, null=True, verbose_name='Narxi'),
        ),
        migrations.AlterField(
            model_name='expensedehqon',
            name='quantity',
            field=models.BigIntegerField(blank=True, null=True, verbose_name='Soni'),
        ),
        migrations.AlterField(
            model_name='incomedehqon',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Qabul qilib olingan sanasi'),
        ),
        migrations.CreateModel(
            name='IncomeBazarOther',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(blank=True, null=True, verbose_name='Soni')),
                ('weight', models.FloatField(blank=True, null=True, verbose_name="Og'irligi")),
                ('price', models.IntegerField(blank=True, default=0, null=True, verbose_name='Sotib olingan Narxi')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(blank=True, choices=[('progress', 'Jarayonda'), ('completed', 'yakunlandi')], default='progress', max_length=88, null=True, verbose_name='Holati')),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='app.product', verbose_name='Mahsulot')),
            ],
            options={
                'verbose_name': "Bozor to'lovi",
                'verbose_name_plural': "Bozor to'lovlari",
                'ordering': ['-created_date'],
            },
        ),
    ]
