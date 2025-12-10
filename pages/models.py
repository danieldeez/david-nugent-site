from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField

class Lead(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=40, blank=True)
    message = models.TextField()
    consent = models.BooleanField(default=False)
    source = models.CharField(max_length=50, default="contact_form")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} <{self.email}>"

class Booking(models.Model):
    calendly_id   = models.CharField(max_length=120, unique=True)
    status        = models.CharField(max_length=30)  # created, canceled
    start_time    = models.DateTimeField(null=True, blank=True)
    end_time      = models.DateTimeField(null=True, blank=True)
    invitee_name  = models.CharField(max_length=120, blank=True)
    invitee_email = models.EmailField(blank=True)
    created_at    = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.invitee_name} ({self.status})"

class HomepageSettings(models.Model):
    """
    Singleton model for homepage hero content.
    Only one instance should exist (pk=1).
    """
    hero_heading = models.CharField(max_length=200, default="Clear, practical legal advice")
    hero_subheading = models.TextField(default="Focused expertise in commercial, criminal, general practice, and personal injury matters. Direct Professional Access provided.")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Homepage Settings"
        verbose_name_plural = "Homepage Settings"

    def __str__(self):
        return "Homepage Settings"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

class TimeStamped(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

class SitePage(TimeStamped):
    """
    Simple CMS pages like About, Privacy, Terms.
    Create one per slug in the admin and your templates will render them.
    """
    slug = models.SlugField(unique=True, help_text="about, privacy, terms")
    title = models.CharField(max_length=180)
    body = RichTextField(blank=True)
    hero_image = models.ImageField(upload_to="pages/", blank=True)

    def __str__(self): return self.title

    @classmethod
    def get_or_create_page(cls, slug, title, body=""):
        """Convenience method to get or create a site page with defaults."""
        page, created = cls.objects.get_or_create(
            slug=slug,
            defaults={"title": title, "body": body}
        )
        return page

class PracticeArea(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    short_summary = models.CharField(max_length=255, blank=True, help_text="Brief summary for practice area cards (1-2 lines)")
    description = models.TextField(blank=True, help_text="DEPRECATED: Use 'body' field instead")
    body = RichTextField(blank=True, help_text="Full description with formatting for the detail page")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("practice_area_detail", args=[self.slug])

class PostBase(TimeStamped):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    summary = models.TextField(blank=True)
    body = RichTextField()
    hero_image = models.ImageField(upload_to="posts/", blank=True)
    published = models.BooleanField(default=True)
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True
        ordering = ["-published_at", "-created_at"]

    def __str__(self): return self.title

class BlogPost(PostBase):
    source_name = models.CharField(max_length=120, blank=True)
    source_url = models.URLField(blank=True)

    def get_absolute_url(self):
        return reverse("blog_detail", args=[self.slug])

class CaseStudy(PostBase):
    practice_areas = models.ManyToManyField(PracticeArea, blank=True)
    outcome = models.CharField(max_length=200, blank=True)
    date_of_case = models.DateField(null=True, blank=True)
    citation_ref = models.CharField(max_length=200, blank=True)
    citation_name = models.CharField(max_length=150, blank=True)
    citation_url = models.URLField(blank=True)

    def get_absolute_url(self):
        return reverse("case_detail", args=[self.slug])

class AvailabilitySlot(models.Model):
    """
    Represents owner-defined availability windows for consultations.
    Part of the custom booking system.
    """
    SLOT_TYPE_CHOICES = [
        ('initial', 'Initial Consultation'),
        ('followup', 'Follow-up'),
        ('general', 'General'),
    ]

    date = models.DateField(help_text="Date of availability")
    start_time = models.TimeField(help_text="Start time (e.g., 14:00)")
    end_time = models.TimeField(help_text="End time (e.g., 15:00)")
    slot_type = models.CharField(
        max_length=50,
        choices=SLOT_TYPE_CHOICES,
        default='initial',
        help_text="Type of consultation"
    )
    is_available = models.BooleanField(
        default=True,
        help_text="Whether this slot is currently bookable"
    )
    notes = models.TextField(blank=True, help_text="Internal notes (not visible to public)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date', 'start_time']
        verbose_name = "Availability Slot"
        verbose_name_plural = "Availability Slots"

    def __str__(self):
        return f"{self.date} {self.start_time.strftime('%H:%M')}-{self.end_time.strftime('%H:%M')} ({self.get_slot_type_display()})"

    def get_formatted_time(self):
        """Returns formatted time range for display (e.g., '2:00 PM - 3:00 PM')"""
        from datetime import datetime
        start = datetime.combine(self.date, self.start_time)
        end = datetime.combine(self.date, self.end_time)
        return f"{start.strftime('%-I:%M %p')} - {end.strftime('%-I:%M %p')}"

    def duration_minutes(self):
        """Calculate duration in minutes from start and end times"""
        from datetime import datetime, timedelta
        start_dt = datetime.combine(self.date, self.start_time)
        end_dt = datetime.combine(self.date, self.end_time)
        delta = end_dt - start_dt
        return int(delta.total_seconds() / 60)

    def is_in_past(self):
        """Check if this slot's date/time has already passed"""
        from datetime import datetime
        from django.utils import timezone
        slot_datetime = datetime.combine(self.date, self.end_time)
        # Make timezone-aware
        slot_datetime = timezone.make_aware(slot_datetime)
        return timezone.now() > slot_datetime

class BookingSubmission(models.Model):
    """
    Represents a client booking submission for a specific availability slot.
    Part of the custom booking system.
    """
    slot = models.ForeignKey(
        AvailabilitySlot,
        on_delete=models.CASCADE,
        related_name="bookings",
        help_text="The availability slot being booked"
    )
    name = models.CharField(max_length=120, help_text="Client name")
    email = models.EmailField(help_text="Client email address")
    phone = models.CharField(max_length=50, blank=True, help_text="Client phone number (optional)")
    description = models.TextField(help_text="Brief description of the matter")
    is_paid = models.BooleanField(default=False, help_text="Whether payment has been received")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Booking Submission"
        verbose_name_plural = "Booking Submissions"

    def __str__(self):
        return f"{self.name} – {self.slot.date} {self.slot.start_time.strftime('%H:%M')}"