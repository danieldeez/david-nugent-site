from django.contrib import admin
from .models import Lead, SitePage, PracticeArea, BlogPost, CaseStudy, Booking, HomepageSettings, AvailabilitySlot, BookingSubmission

@admin.register(HomepageSettings)
class HomepageSettingsAdmin(admin.ModelAdmin):
    list_display = ("hero_heading", "updated_at")

    def has_add_permission(self, request):
        # Only allow one instance
        return not HomepageSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # Prevent deletion
        return False

@admin.register(SitePage)
class SitePageAdmin(admin.ModelAdmin):
    list_display = ("title","slug","updated_at")
    search_fields = ("title","body")
    prepopulated_fields = {"slug": ("title",)}

@admin.register(PracticeArea)
class PracticeAreaAdmin(admin.ModelAdmin):
    list_display = ("name","order")
    prepopulated_fields = {"slug": ("name",)}
    list_editable = ("order",)

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title","published","published_at","created_at","source_name")
    list_filter = ("published",)
    search_fields = ("title","summary","body","source_name")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "published_at"
    fieldsets = (
        (None, {
            "fields": ("title", "slug", "summary", "body", "hero_image")
        }),
        ("Source Attribution", {
            "fields": ("source_name", "source_url"),
            "classes": ("collapse",),
        }),
        ("Publication", {
            "fields": ("published", "published_at")
        }),
    )

@admin.register(CaseStudy)
class CaseStudyAdmin(admin.ModelAdmin):
    list_display = ("title","outcome","published","published_at")
    list_filter = ("published","practice_areas")
    search_fields = ("title","summary","body","citation_ref","citation_name")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("practice_areas",)
    date_hierarchy = "published_at"
    fieldsets = (
        (None, {
            "fields": ("title", "slug", "summary", "body", "hero_image")
        }),
        ("Case Information", {
            "fields": ("practice_areas", "outcome", "date_of_case", "citation_ref")
        }),
        ("Reference (Optional)", {
            "fields": ("citation_name", "citation_url"),
            "classes": ("collapse",),
        }),
        ("Publication", {
            "fields": ("published", "published_at")
        }),
    )

@admin.register(AvailabilitySlot)
class AvailabilitySlotAdmin(admin.ModelAdmin):
    list_display = ("date", "start_time", "end_time", "slot_type", "is_available", "created_at")
    list_filter = ("is_available", "slot_type", "date")
    search_fields = ("notes",)
    date_hierarchy = "date"
    list_editable = ("is_available",)
    ordering = ("date", "start_time")

@admin.register(BookingSubmission)
class BookingSubmissionAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "slot", "is_paid", "created_at")
    list_filter = ("is_paid", "created_at", "slot__date")
    search_fields = ("name", "email", "phone", "description")
    readonly_fields = ("created_at",)
    list_editable = ("is_paid",)
    date_hierarchy = "created_at"
    ordering = ("-created_at",)
    fieldsets = (
        ("Client Information", {
            "fields": ("name", "email", "phone")
        }),
        ("Booking Details", {
            "fields": ("slot", "description")
        }),
        ("Payment & Status", {
            "fields": ("is_paid", "created_at")
        }),
    )