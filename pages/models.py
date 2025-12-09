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