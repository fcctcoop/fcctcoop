# Generated by Django 3.2.3 on 2021-10-01 09:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0007_auto_20211001_0918'),
    ]

    operations = [
        migrations.RenameField(
            model_name='client',
            old_name='branchcode',
            new_name='client_branchcode',
        ),
        migrations.RenameField(
            model_name='client',
            old_name='zipcode',
            new_name='client_zipcode',
        ),
    ]