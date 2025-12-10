from django import forms
from .models import Lead, HomepageSettings, SitePage, PracticeArea, BlogPost, CaseStudy, AvailabilitySlot, BookingSubmission

class ContactForm(forms.ModelForm):
    consent = forms.BooleanField(
        required=True,
        label="I agree to the Privacy Policy and understand this is not legal advice."
    )

    class Meta:
        model = Lead
        fields = ["name", "email", "phone", "message", "consent"]
        widgets = {"message": forms.Textarea(attrs={"rows": 5})}

class HomepageSettingsForm(forms.ModelForm):
    class Meta:
        model = HomepageSettings
        fields = ["hero_heading", "hero_subheading"]
        widgets = {
            "hero_heading": forms.TextInput(attrs={"class": "form-control", "placeholder": "Main heading"}),
            "hero_subheading": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Subheading or tagline"}),
        }
        labels = {
            "hero_heading": "Hero Heading",
            "hero_subheading": "Hero Subheading",
        }

class AboutPageForm(forms.ModelForm):
    class Meta:
        model = SitePage
        fields = ["title", "body", "hero_image"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Page title"}),
            "body": forms.Textarea(attrs={"class": "form-control", "rows": 12, "placeholder": "Page content"}),
        }
        labels = {
            "title": "About Page Title",
            "body": "About Page Content",
            "hero_image": "Portrait/Headshot Image",
        }
        help_texts = {
            "hero_image": "Upload a professional portrait or headshot (recommended: square or 3:4 ratio, at least 600x800px).",
        }

class SitePageForm(forms.ModelForm):
    class Meta:
        model = SitePage
        fields = ["title", "body"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Page title"}),
            "body": forms.Textarea(attrs={"class": "form-control", "rows": 15, "placeholder": "Page content (HTML allowed)"}),
        }
        labels = {
            "title": "Page Title",
            "body": "Page Content",
        }
        help_texts = {
            "body": "HTML formatting is supported. Use the rich text editor for easier formatting.",
        }

class PracticeAreaForm(forms.ModelForm):
    class Meta:
        model = PracticeArea
        fields = ["name", "slug", "short_summary", "body", "order"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g., Commercial Litigation"}),
            "slug": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g., commercial-litigation"}),
            "short_summary": forms.TextInput(attrs={"class": "form-control", "placeholder": "Brief one-line summary for practice area cards"}),
            "order": forms.NumberInput(attrs={"class": "form-control", "placeholder": "0"}),
        }
        help_texts = {
            "slug": "Used in the URL. Lowercase with hyphens, e.g., 'employment-law'.",
            "short_summary": "Short summary shown on the Practice Areas cards (max 2 lines, ~160 characters).",
            "body": "Full description with formatting for the Practice Area detail page. You may use rich text formatting.",
            "order": "Lower numbers appear first. Use 0, 10, 20, etc. to allow easy reordering.",
        }

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ["title", "slug", "summary", "source_name", "source_url", "body", "hero_image", "published", "published_at"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g., Understanding Employment Contracts"}),
            "slug": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g., understanding-employment-contracts"}),
            "summary": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Brief summary for the blog listing page"}),
            "source_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g., Irish Times, Courts.ie"}),
            "source_url": forms.URLInput(attrs={"class": "form-control", "placeholder": "https://..."}),
            "published_at": forms.DateTimeInput(attrs={"class": "form-control", "type": "datetime-local"}),
        }
        help_texts = {
            "slug": "Used in the blog post URL. Lowercase with hyphens, e.g., 'my-blog-post'.",
            "summary": "A short excerpt shown on the blog listing page.",
            "source_name": "e.g., Irish Times, Courts.ie",
            "source_url": "Link to external article or judgment",
            "published": "Uncheck to save as draft (not visible to public).",
            "published_at": "Optional: Schedule when this post should be considered published.",
            "hero_image": "Optional: Featured image for the blog post.",
        }

class CaseStudyForm(forms.ModelForm):
    class Meta:
        model = CaseStudy
        fields = ["title", "slug", "summary", "body", "hero_image", "practice_areas", "outcome", "date_of_case", "citation_ref", "citation_name", "citation_url", "published", "published_at"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g., Smith v. Jones Ltd"}),
            "slug": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g., smith-v-jones-ltd"}),
            "summary": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Brief case summary"}),
            "outcome": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g., Successful settlement"}),
            "date_of_case": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "citation_ref": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g., [2024] IEHC 123"}),
            "citation_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g., Courts.ie, Irish Times"}),
            "citation_url": forms.URLInput(attrs={"class": "form-control", "placeholder": "https://..."}),
            "published_at": forms.DateTimeInput(attrs={"class": "form-control", "type": "datetime-local"}),
            "practice_areas": forms.CheckboxSelectMultiple(),
        }
        help_texts = {
            "slug": "Used in the case URL. Lowercase with hyphens, e.g., 'my-case-study'.",
            "summary": "A short excerpt shown on the cases listing page.",
            "outcome": "The result or settlement achieved.",
            "date_of_case": "Date the case was heard or settled.",
            "citation_ref": "Official case citation if applicable.",
            "citation_name": "e.g., Courts.ie, Irish Times (optional)",
            "citation_url": "Official judgment or media article (optional)",
            "practice_areas": "Select all relevant practice areas.",
            "published": "Uncheck to save as draft (not visible to public).",
            "published_at": "Optional: Schedule when this case study should be published.",
            "hero_image": "Optional: Featured image for the case study.",
        }

class AvailabilitySlotForm(forms.ModelForm):
    class Meta:
        model = AvailabilitySlot
        fields = ["date", "start_time", "end_time", "slot_type", "is_available", "notes"]
        widgets = {
            "date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "start_time": forms.TimeInput(attrs={"class": "form-control", "type": "time"}),
            "end_time": forms.TimeInput(attrs={"class": "form-control", "type": "time"}),
            "slot_type": forms.Select(attrs={"class": "form-select"}),
            "is_available": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "notes": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Optional internal notes"}),
        }
        labels = {
            "date": "Date",
            "start_time": "Start Time",
            "end_time": "End Time",
            "slot_type": "Consultation Type",
            "is_available": "Available for booking",
            "notes": "Internal Notes",
        }
        help_texts = {
            "date": "Select the date for this availability slot.",
            "start_time": "Start time of the slot (e.g., 14:00).",
            "end_time": "End time of the slot (e.g., 15:00). Must be after start time.",
            "slot_type": "Type of consultation this slot is for.",
            "is_available": "Uncheck to temporarily disable this slot without deleting it.",
            "notes": "Private notes for your reference (not visible to clients).",
        }

    def clean(self):
        """Validate that end_time is after start_time"""
        cleaned_data = super().clean()
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")

        if start_time and end_time:
            if end_time <= start_time:
                raise forms.ValidationError("End time must be after start time.")

        return cleaned_data

class BookingSubmissionForm(forms.ModelForm):
    class Meta:
        model = BookingSubmission
        fields = ["name", "email", "phone", "description"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Your full name"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "your.email@example.com"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "+353 (optional)"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 5, "placeholder": "Briefly describe your legal matter..."}),
        }
        labels = {
            "name": "Full Name",
            "email": "Email Address",
            "phone": "Phone Number",
            "description": "Brief Description of Your Matter",
        }
        help_texts = {
            "name": "Your full name as it should appear on the booking.",
            "email": "We'll send confirmation to this email address.",
            "phone": "Optional. Provide if you'd like to be contacted by phone.",
            "description": "Provide a brief overview of your legal matter (2-3 sentences).",
        }
