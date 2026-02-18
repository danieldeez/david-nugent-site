import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0013_intakesession'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookingsubmission',
            name='intake',
            field=models.ForeignKey(
                blank=True,
                help_text='Optional link to the intake session that led to this booking',
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='bookings',
                to='pages.intakesession',
            ),
        ),
    ]
