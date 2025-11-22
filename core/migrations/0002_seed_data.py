from django.db import migrations
from django.utils import timezone


def seed_forward(apps, schema_editor):
    # Skip seeding data during deployment
    pass


def seed_backward(apps, schema_editor):
    # Skip cleanup during rollback
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_forward, seed_backward),
    ]


