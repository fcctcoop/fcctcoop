# Generated by Django 3.2.3 on 2021-10-05 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mmaptsp2', '0003_remove_mmap_branch_control_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mmap',
            name='clientid',
        ),
        migrations.AddField(
            model_name='mmap',
            name='client_code',
            field=models.CharField(blank=True, default='NONE', max_length=15, verbose_name='Client Code '),
        ),
    ]