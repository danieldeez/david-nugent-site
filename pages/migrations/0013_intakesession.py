import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0012_bookingsubmission'),
    ]

    operations = [
        migrations.CreateModel(
            name='IntakeSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('name', models.CharField(blank=True, help_text='Optional user name', max_length=200)),
                ('email', models.EmailField(blank=True, help_text='Optional user email', max_length=254)),
                ('raw_text', models.TextField(help_text="User's free-text description of their matter")),
                ('structured_output', models.JSONField(blank=True, help_text='AI-generated structured data', null=True)),
                ('recommended_slot_type', models.CharField(blank=True, help_text='AI-recommended consultation type', max_length=100)),
                ('is_suitable', models.BooleanField(blank=True, help_text='AI suitability assessment', null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Intake Session',
                'verbose_name_plural': 'Intake Sessions',
                'ordering': ['-created_at'],
            },
        ),
    ]
