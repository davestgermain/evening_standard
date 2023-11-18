# Generated by Django 4.2.6 on 2023-11-18 18:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("wagtaildocs", "0012_uploadeddocument"),
        ("shows", "0005_venue_website"),
    ]

    operations = [
        migrations.CreateModel(
            name="Listen",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("start", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("ip_address", models.GenericIPAddressField()),
                ("browser", models.CharField(default="unknown", max_length=255)),
                ("referer", models.CharField(default="", max_length=255)),
                (
                    "document",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="wagtaildocs.document",
                    ),
                ),
            ],
        ),
    ]
