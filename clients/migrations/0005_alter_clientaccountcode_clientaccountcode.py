# Generated by Django 3.2.3 on 2021-09-30 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0004_alter_clientaccountcode_branchcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientaccountcode',
            name='clientaccountcode',
            field=models.CharField(blank=True, max_length=5, verbose_name='Client Account Number'),
        ),
    ]