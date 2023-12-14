# Generated by Django 5.0 on 2023-12-14 11:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('age', models.IntegerField(default=18)),
                ('phone', models.CharField(max_length=20, unique=True)),
                ('monthaly_salary', models.IntegerField()),
                ('approved_limit', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loan_amount', models.IntegerField()),
                ('tenure', models.IntegerField()),
                ('interest_rate', models.FloatField()),
                ('emi', models.FloatField()),
                ('emi_paid_on_time', models.SmallIntegerField(default=0)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='loans', to='core.customer')),
            ],
        ),
    ]
