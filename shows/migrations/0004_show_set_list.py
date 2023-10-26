# Generated by Django 4.2.6 on 2023-10-25 22:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('setlist', '0002_alter_setsong_unique_together'),
        ('shows', '0003_showindex_show_recordings'),
    ]

    operations = [
        migrations.AddField(
            model_name='show',
            name='set_list',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='setlist.setlist'),
        ),
    ]
