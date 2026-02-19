from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.conf import settings
from django.contrib import messages
from .forms import ContactForm, IntakeForm, HomepageSettingsForm, AboutPageForm, SitePageForm, PracticeAreaForm, BlogPostForm, CaseStudyForm, AvailabilitySlotForm, BookingSubmissionForm
import hmac, hashlib, json
import re, time, requests
from datetime import datetime, timedelta, timezone as dt_tz
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse, HttpResponseBadRequest
from .models import Booking, HomepageSettings, PracticeArea
from .models import SitePage, PracticeArea, BlogPost, CaseStudy, IntakeSession, AvailabilitySlot, BookingSubmission
from django.core.cache import cache
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from pathlib import Path
from .llm_utils import call_llm_json, LLMError

def home(request):
    homepage = HomepageSettings.load()
    practice_areas = PracticeArea.objects.all()[:3]
    featured_cases = CaseStudy.objects.filter(published=True).order_by('-published_at')[:3]
    latest_posts = BlogPost.objects.filter(published=True).order_by('-published_at')[:3]
    return render(request, "SitePages/home.html", {
        "homepage": homepage,
        "practice_areas": practice_areas,
        "featured_cases": featured_cases,
        "latest_posts": latest_posts,
    })

def about(request):
    page, created = SitePage.objects.get_or_create(
        slug="about",
        defaults={"title": "About", "body": ""}
    )
    return render(request, "SitePages/about.html", {"page": page})

def privacy(request):
    page = SitePage.get_or_create_page(
        slug="privacy",
        title="Privacy Policy",
        body="<p>This is a placeholder privacy policy. Please update this content from the Owner area.</p>"
    )
    return render(request, "SitePages/privacy.html", {"page": page})

def terms(request):
    page = SitePage.get_or_create_page(
        slug="terms",
        title="Terms of Use",
        body="<p>This is a placeholder terms of use. Please update this content from the Owner area.</p>"
    )
    return render(request, "SitePages/terms.html", {"page": page})

def contact(request):
    if request.method == "POST":
        form = IntakeForm(request.POST)
        if form.is_valid():
            intake_session = form.save()
            return redirect("intake_thank_you", intake_uuid=intake_session.uuid)
    else:
        form = IntakeForm()
    return render(request, "SitePages/contact.html", {"form": form})

def calendly_webhook(request):
    if request.method != "POST":
        return HttpResponse(status=405)

    # Verify Calendly signature (Settings → Webhooks → Signing Key)
    signing_key = getattr(settings, "CALENDLY_SIGNING_KEY", "")
    if signing_key:
        sig = request.headers.get("Calendly-Webhook-Signature", "")
        try:
            parts = dict(p.split("=",1) for p in sig.split(","))
            expected = hmac.new(signing_key.encode(), msg=request.body, digestmod=hashlib.sha256).hexdigest()
            if parts.get("v1") != expected:
                return HttpResponseForbidden("Invalid signature")
        except Exception:
            return HttpResponseForbidden("Bad signature header")

    payload = json.loads(request.body.decode("utf-8"))
    trig = payload.get("event")            # e.g. "invitee.created"
    data = payload.get("payload", {})

    # Common fields (v2 webhooks)
    event = data.get("event", {})          # start_time, end_time, status
    invitee = data.get("invitee", {})      # name, email
    uid = invitee.get("uuid") or data.get("uuid") or event.get("uuid") or "unknown"

    if trig == "invitee.created":
        Booking.objects.update_or_create(
            calendly_id=uid,
            defaults={
                "status": "created",
                "start_time": event.get("start_time"),
                "end_time": event.get("end_time"),
                "invitee_name": invitee.get("name",""),
                "invitee_email": invitee.get("email",""),
            }
        )
    elif trig == "invitee.canceled":
        Booking.objects.update_or_create(
            calendly_id=uid,
            defaults={"status": "canceled"}
        )

    return HttpResponse(status=204)

def page_view(slug):
    def view(request):
        page = get_object_or_404(SitePage, slug=slug)
        return render(request, "SitePages/page_generic.html", {"page": page})
    return view

def practice_areas(request):
    areas = PracticeArea.objects.all()
    return render(request, "SitePages/practice_areas.html", {"areas": areas})

def practice_area_detail(request, slug):
    area = get_object_or_404(PracticeArea, slug=slug)
    all_areas = PracticeArea.objects.all()
    return render(request, "SitePages/practice_area_detail.html", {"area": area, "all_areas": all_areas})

# Blog
def blog_list(request):
    posts = BlogPost.objects.filter(published=True).order_by('-published_at', '-id')
    return render(request, "SitePages/blog_list.html", {"posts": posts})

def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, published=True)
    return render(request, "SitePages/blog_detail.html", {"post": post})

# Cases
def case_list(request):
    cases = CaseStudy.objects.filter(published=True).order_by('-published_at', '-id')
    return render(request, "SitePages/case_list.html", {"cases": cases})

def case_detail(request, slug):
    case = get_object_or_404(CaseStudy, slug=slug, published=True)
    return render(request, "SitePages/case_detail.html", {"case": case})

# Intake System
def intake_start(request):
    if request.method == "POST":
        form = IntakeForm(request.POST)
        if form.is_valid():
            intake_session = form.save()
            return redirect("intake_thank_you", intake_uuid=intake_session.uuid)
    else:
        form = IntakeForm()
    return render(request, "SitePages/intake_start.html", {"form": form})

def classify_intake_session(session):
    if session.is_suitable is not None:
        return True
    prompt_file = Path(settings.BASE_DIR) / "ai" / "prompts" / "intake_classify.txt"
    try:
        system_prompt = prompt_file.read_text(encoding="utf-8")
    except FileNotFoundError:
        return False
    try:
        result = call_llm_json(
            system_prompt=system_prompt,
            user_prompt=session.raw_text,
            temperature=0.1,
            max_tokens=100,
            timeout=10
        )
        session.is_suitable = result.get("is_suitable", None)
        if session.structured_output is None:
            session.structured_output = {}
        session.structured_output["triage"] = result
        session.save()
        return True
    except (LLMError, Exception):
        return False

def intake_thank_you(request, intake_uuid):
    intake_session = get_object_or_404(IntakeSession, uuid=intake_uuid)
    classify_intake_session(intake_session)
    return render(request, "SitePages/intake_thank_you.html", {"intake_session": intake_session})

# Owner area
def is_staff_user(user):
    return user.is_authenticated and user.is_staff

@login_required
@user_passes_test(is_staff_user, login_url='/')
def owner_dashboard(request):
    return render(request, "SitePages/owner_dashboard.html")

@login_required
@user_passes_test(is_staff_user, login_url='/')
def owner_edit_homepage(request):
    homepage = HomepageSettings.load()
    if request.method == "POST":
        form = HomepageSettingsForm(request.POST, instance=homepage)
        if form.is_valid():
            form.save()
            messages.success(request, "Homepage hero content updated successfully!")
            return redirect("owner_dashboard")
    else:
        form = HomepageSettingsForm(instance=homepage)
    return render(request, "SitePages/owner_homepage_form.html", {"form": form})

@login_required
@user_passes_test(is_staff_user, login_url='/')
def owner_edit_about(request):
    page, created = SitePage.objects.get_or_create(
        slug="about",
        defaults={"title": "About", "body": ""}
    )
    if request.method == "POST":
        form = AboutPageForm(request.POST, request.FILES, instance=page)
        if form.is_valid():
            form.save()
            messages.success(request, "About page updated successfully!")
            return redirect("owner_dashboard")
    else:
        form = AboutPageForm(instance=page)
    return render(request, "SitePages/owner_about_form.html", {"form": form})

@login_required
@user_passes_test(is_staff_user, login_url='/')
def owner_site_pages_list(request):
    pages = SitePage.objects.exclude(slug="about").order_by("slug")
    return render(request, "SitePages/owner_site_pages_list.html", {"pages": pages})

@login_required
@user_passes_test(is_staff_user, login_url='/')
def owner_edit_site_page(request, slug):
    # Known pages with default content
    defaults = {
        "privacy": {"title": "Privacy Policy", "body": "<p>Please add your privacy policy content here.</p>"},
        "terms": {"title": "Terms of Use", "body": "<p>Please add your terms of use content here.</p>"},
    }

    page, created = SitePage.objects.get_or_create(
        slug=slug,
        defaults=defaults.get(slug, {"title": slug.replace("-", " ").title(), "body": ""})
    )

    if request.method == "POST":
        form = SitePageForm(request.POST, instance=page)
        if form.is_valid():
            form.save()
            messages.success(request, f"'{page.title}' updated successfully!")
            return redirect("owner_site_pages")
    else:
        form = SitePageForm(instance=page)

    return render(request, "SitePages/owner_site_page_form.html", {"form": form, "page": page})

@login_required
@user_passes_test(is_staff_user, login_url='/')
def owner_practice_area_list(request):
    areas = PracticeArea.objects.all()
    return render(request, "SitePages/owner_practice_area_list.html", {"areas": areas})

@login_required
@user_passes_test(is_staff_user, login_url='/')
def owner_practice_area_create(request):
    if request.method == "POST":
        form = PracticeAreaForm(request.POST)
        if form.is_valid():
            area = form.save()
            messages.success(request, f"Practice area '{area.name}' created successfully!")
            return redirect("owner_practice_area_list")
    else:
        form = PracticeAreaForm()
    return render(request, "SitePages/owner_practice_area_form.html", {
        "form": form,
        "is_create": True
    })

@login_required
@user_passes_test(is_staff_user, login_url='/')
def owner_practice_area_edit(request, pk):
    area = get_object_or_404(PracticeArea, pk=pk)

    if request.method == "POST":
        form = PracticeAreaForm(request.POST, instance=area)
        if form.is_valid():
            form.save()
            messages.success(request, f"Practice area '{area.name}' updated successfully!")
            return redirect("owner_practice_area_list")
    else:
        form = PracticeAreaForm(instance=area)

    return render(request, "SitePages/owner_practice_area_form.html", {
        "form": form,
        "area": area,
        "is_create": False
    })

@login_required
@user_passes_test(is_staff_user, login_url='/')
def owner_practice_area_delete(request, pk):
    area = get_object_or_404(PracticeArea, pk=pk)

    if request.method == "POST":
        name = area.name
        area.delete()
        messages.success(request, f"Practice area '{name}' deleted successfully.")
        return redirect("owner_practice_area_list")

    return render(request, "SitePages/owner_practice_area_confirm_delete.html", {"area": area})

@login_required
@user_passes_test(is_staff_user, login_url='/')
def owner_intake_list(request):
    intake_sessions = IntakeSession.objects.all()
    return render(request, "SitePages/owner_intake_list.html", {"intake_sessions": intake_sessions})

@login_required
@user_passes_test(is_staff_user, login_url='/')
def owner_intake_detail(request, intake_uuid):
    intake_session = get_object_or_404(IntakeSession, uuid=intake_uuid)
    structured = intake_session.structured_output or {}
    linked_bookings = intake_session.bookings.all().select_related('slot').order_by('-created_at')
    return render(request, "SitePages/owner_intake_detail.html", {
        "intake_session": intake_session,
        "structured": structured,
        "linked_bookings": linked_bookings,
    })

@login_required
@user_passes_test(is_staff_user, login_url='/')
def owner_intake_analyse(request, intake_uuid):
    intake_session = get_object_or_404(IntakeSession, uuid=intake_uuid)
    if request.method != "POST":
        return redirect("owner_intake_list")
    prompt_file = Path(settings.BASE_DIR) / "ai" / "prompts" / "intake_prompt.txt"
    try:
        system_prompt = prompt_file.read_text(encoding="utf-8")
    except FileNotFoundError:
        messages.error(request, "AI intake prompt file not found. Please check configuration.")
        return redirect("owner_intake_list")
    try:
        result = call_llm_json(
            system_prompt=system_prompt,
            user_prompt=intake_session.raw_text,
            temperature=0.2,
            max_tokens=1500,
            timeout=30
        )
        intake_session.structured_output = result
        intake_session.save()
        messages.success(request, "AI analysis completed successfully.")
        return redirect("owner_intake_detail", intake_uuid=intake_uuid)
    except LLMError as e:
        messages.error(request, f"AI analysis failed: {str(e)}")
        return redirect("owner_intake_list")
    except Exception as e:
        messages.error(request, f"Unexpected error during AI analysis: {str(e)}")
        return redirect("owner_intake_list")

@login_required
@user_passes_test(is_staff_user, login_url='/')
def owner_blog_list(request):
    posts = BlogPost.objects.all()
    return render(request, "SitePages/owner_blog_list.html", {"posts": posts})

@login_required
@user_passes_test(is_staff_user, login_url='/')
def owner_blog_create(request):
    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save()
            messages.success(request, f"Blog post '{post.title}' created successfully!")
            return redirect("owner_blog_list")
    else:
        form = BlogPostForm()
    return render(request, "SitePages/owner_blog_form.html", {
        "form": form,
        "is_create": True
    })

@login_required
@user_passes_test(is_staff_user, login_url='/')
def owner_blog_edit(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)

    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, f"Blog post '{post.title}' updated successfully!")
            return redirect("owner_blog_list")
    else:
        form = BlogPostForm(instance=post)

    return render(request, "SitePages/owner_blog_form.html", {
        "form": form,
        "post": post,
        "is_create": False
    })

@login_required
@user_passes_test(is_staff_user, login_url='/')
def owner_blog_delete(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)

    if request.method == "POST":
        title = post.title
        post.delete()
        messages.success(request, f"Blog post '{title}' deleted successfully.")
        return redirect("owner_blog_list")

    return render(request, "SitePages/owner_blog_confirm_delete.html", {"post": post})

@login_required
@user_passes_test(is_staff_user, login_url='/')
def owner_case_list(request):
    cases = CaseStudy.objects.all()
    return render(request, "SitePages/owner_case_list.html", {"cases": cases})

@login_required
@user_passes_test(is_staff_user, login_url='/')
def owner_case_create(request):
    if request.method == "POST":
        form = CaseStudyForm(request.POST, request.FILES)
        if form.is_valid():
            case = form.save()
            messages.success(request, f"Case study '{case.title}' created successfully!")
            return redirect("owner_case_list")
    else:
        form = CaseStudyForm()
    return render(request, "SitePages/owner_case_form.html", {
        "form": form,
        "is_create": True
    })

@login_required
@user_passes_test(is_staff_user, login_url='/')
def owner_case_edit(request, pk):
    case = get_object_or_404(CaseStudy, pk=pk)

    if request.method == "POST":
        form = CaseStudyForm(request.POST, request.FILES, instance=case)
        if form.is_valid():
            form.save()
            messages.success(request, f"Case study '{case.title}' updated successfully!")
            return redirect("owner_case_list")
    else:
        form = CaseStudyForm(instance=case)

    return render(request, "SitePages/owner_case_form.html", {
        "form": form,
        "case": case,
        "is_create": False
    })

@login_required
@user_passes_test(is_staff_user, login_url='/')
def owner_case_delete(request, pk):
    case = get_object_or_404(CaseStudy, pk=pk)

    if request.method == "POST":
        title = case.title
        case.delete()
        messages.success(request, f"Case study '{title}' deleted successfully.")
        return redirect("owner_case_list")

    return render(request, "SitePages/owner_case_confirm_delete.html", {"case": case})

SYSTEM_PROMPT = """You are a website assistant for barrister David Nugent.

RULES:
- Provide general, high-level information only. Do NOT give legal advice.
- If the user asks for case-specific guidance, politely decline and suggest booking a consultation.
- Jurisdiction: Ireland (unless user explicitly states otherwise).
- Do not collect sensitive personal data. If user shares it, warn and redirect to the contact form or booking.
- Tone: professional, warm, concise, plain English. Keep answers short (2–5 sentences) with clear CTAs when helpful.
- If unsure, say so and suggest booking.

INTERNAL LINKS:
- You may include internal links using HTML anchor tags: <a href="/path/">link text</a>
- ONLY link to URLs listed in the SITE MAP below, or to top-level pages: /about/, /contact/, /book/, /practice-areas/, /blog/, /cases/
- Do NOT invent or guess URLs. If unsure whether a specific page exists, link to the nearest parent page.
- Example: "You can learn more about employment matters <a href='/practice-areas/employment/'>here</a>."
- Example: "To book a consultation, visit the <a href='/book/'>booking page</a>."
"""

def _build_site_context():
    """
    Build a structured site map with real URLs from the database.
    Returns a formatted string for injection into the system prompt.
    """
    parts = []

    # Static pages (always available)
    parts.append("SITE MAP - Static Pages:")
    parts.append("- About: /about/")
    parts.append("- Contact: /contact/")
    parts.append("- Book Consultation: /book/")
    parts.append("- Practice Areas Index: /practice-areas/")
    parts.append("- Blog Index: /blog/")
    parts.append("- Case Studies Index: /cases/")
    parts.append("- Privacy Policy: /privacy/")
    parts.append("- Terms of Use: /terms/")
    parts.append("")

    # Practice Areas (with real URLs)
    try:
        areas = PracticeArea.objects.all().order_by("order")[:8]
        if areas:
            parts.append("Practice Areas (detailed pages):")
            for area in areas:
                url = f"/practice-areas/{area.slug}/"
                parts.append(f"- {area.name}: {url}")
            parts.append("")
    except Exception:
        pass

    # Recent Blog Posts
    try:
        posts = BlogPost.objects.filter(published=True).order_by('-published_at')[:6]
        if posts:
            parts.append("Recent Blog Posts:")
            for post in posts:
                parts.append(f"- {post.title}: {post.get_absolute_url()}")
            parts.append("")
    except Exception:
        pass

    # Recent Case Studies
    try:
        cases = CaseStudy.objects.filter(published=True).order_by('-published_at')[:4]
        if cases:
            parts.append("Recent Case Studies:")
            for case in cases:
                parts.append(f"- {case.title}: {case.get_absolute_url()}")
            parts.append("")
    except Exception:
        pass

    return "\n".join(parts)

def _redact_personal(text: str) -> str:
    """Light redaction: strip emails/phones so we don't store/echo them."""
    text = re.sub(r'[\w\.-]+@[\w\.-]+', '[redacted-email]', text)
    text = re.sub(r'\+?\d[\d\s\-\(\)]{7,}\d', '[redacted-phone]', text)
    return text

def _rate_key(request):
    ip = request.META.get("REMOTE_ADDR", "unknown")
    ua = request.META.get("HTTP_USER_AGENT", "")[:60]
    return "assist_rl_" + hashlib.sha256(f"{ip}|{ua}".encode()).hexdigest()

@csrf_exempt
def ai_assist(request):
    if request.method != "POST":
        return JsonResponse({"reply": "POST only"}, status=405)
    if not settings.ASSISTANT_ENABLED:
        return JsonResponse({"reply": "The assistant is currently unavailable. Please use the contact form or book a consultation."})

    # very light per-IP throttle: 1 request / 3 seconds, burst 3 in 30s
    key = _rate_key(request)
    now = time.time()
    window = cache.get(key, {"ts": [], "block": 0})
    # drop old timestamps
    window["ts"] = [t for t in window["ts"] if now - t < 30]
    if window.get("block", 0) and now - window["block"] < 10:
        return JsonResponse({"reply":"You're sending messages a bit quickly—please wait a moment and try again."}, status=200)
    if len(window["ts"]) >= 3:
        window["block"] = now
        cache.set(key, window, 30)
        return JsonResponse({"reply":"You're sending messages a bit quickly—please wait a moment and try again."}, status=200)

    try:
        payload = json.loads(request.body.decode("utf-8"))
        user_msg = (payload.get("message") or "").strip()
        history  = payload.get("history") or []
    except Exception:
        return JsonResponse({"reply": "Invalid request format"}, status=400)

    if not user_msg:
        return JsonResponse({"reply": "Please enter a message"}, status=400)

    # keep short history
    history = history[-8:]

    # Build site-aware context with real URLs
    site_map = _build_site_context()
    system_message = SYSTEM_PROMPT + "\n\n" + site_map

    messages = [
        {"role":"system","content": system_message},
    ] + history + [
        {"role":"user","content": user_msg}
    ]

    # Call OpenAI-compatible endpoint
    try:
        resp = requests.post(
            f"{settings.LLM_BASE_URL}/chat/completions",
            headers={
                "Authorization": f"Bearer {settings.LLM_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": settings.LLM_MODEL,
                "messages": messages,
                "temperature": 0.2,
                "max_tokens": 350,
            },
            timeout=25,
        )
        resp.raise_for_status()
        data = resp.json()
        reply = data["choices"][0]["message"]["content"].strip()
    except Exception:
        reply = ("Sorry—I'm unavailable right now. For anything important, "
                 "please use the contact form or book a consultation.")

    # record a timestamp for rate-limiting window
    window["ts"].append(now)
    cache.set(key, window, 30)

    # light redaction before returning (just in case)
    reply = _redact_personal(reply)

    # Note: Frontend handles HTML sanitization, only allowing safe tags
    # (<a>, <p>, <ul>, <li>, <strong>, <em>) and only internal links (starting with /)
    return JsonResponse({"reply": reply})

# Availability Slots (Custom Booking System)
@login_required
@user_passes_test(is_staff_user, login_url='/')
def owner_availability_list(request):
    slots = AvailabilitySlot.objects.all()
    return render(request, "SitePages/owner_availability_list.html", {"slots": slots})

@login_required
@user_passes_test(is_staff_user, login_url='/')
def owner_availability_create(request):
    if request.method == "POST":
        form = AvailabilitySlotForm(request.POST)
        if form.is_valid():
            slot = form.save()
            messages.success(request, f"Availability slot created successfully for {slot.date} at {slot.start_time.strftime('%H:%M')}!")
            return redirect("owner_availability_list")
    else:
        form = AvailabilitySlotForm()
    return render(request, "SitePages/owner_availability_form.html", {
        "form": form,
        "is_create": True
    })

@login_required
@user_passes_test(is_staff_user, login_url='/')
def owner_availability_edit(request, pk):
    slot = get_object_or_404(AvailabilitySlot, pk=pk)

    if request.method == "POST":
        form = AvailabilitySlotForm(request.POST, instance=slot)
        if form.is_valid():
            form.save()
            messages.success(request, f"Availability slot updated successfully!")
            return redirect("owner_availability_list")
    else:
        form = AvailabilitySlotForm(instance=slot)

    return render(request, "SitePages/owner_availability_form.html", {
        "form": form,
        "slot": slot,
        "is_create": False
    })

@login_required
@user_passes_test(is_staff_user, login_url='/')
def owner_availability_delete(request, pk):
    slot = get_object_or_404(AvailabilitySlot, pk=pk)

    if request.method == "POST":
        date_str = slot.date.strftime("%Y-%m-%d")
        time_str = slot.start_time.strftime("%H:%M")
        slot.delete()
        messages.success(request, f"Availability slot for {date_str} at {time_str} deleted successfully.")
        return redirect("owner_availability_list")

    return render(request, "SitePages/owner_availability_confirm_delete.html", {"slot": slot})

# Public Booking System Views
def book_index(request):
    """Shows list of available dates"""
    from datetime import date
    from collections import defaultdict

    intake_uuid = request.GET.get('intake')

    today = date.today()
    available_slots = AvailabilitySlot.objects.filter(
        date__gte=today,
        is_available=True
    ).order_by('date', 'start_time')

    dates_with_counts = defaultdict(int)
    for slot in available_slots:
        dates_with_counts[slot.date] += 1

    dates_list = sorted(dates_with_counts.items())

    return render(request, "SitePages/booking_index.html", {
        "dates_list": dates_list,
        "intake_uuid": intake_uuid,
    })

def book_date(request, date):
    """Shows available slots for a specific date"""
    from datetime import datetime

    # Parse the date from URL parameter
    try:
        selected_date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        messages.error(request, "Invalid date format.")
        return redirect("book_index")

    # Get available slots for this date
    slots = AvailabilitySlot.objects.filter(
        date=selected_date,
        is_available=True
    ).order_by('start_time')

    if not slots:
        messages.warning(request, "No available slots for this date.")
        return redirect("book_index")

    return render(request, "SitePages/booking_date.html", {
        "selected_date": selected_date,
        "slots": slots,
    })

def book_slot(request, pk):
    """Displays booking form for a specific slot"""
    slot = get_object_or_404(AvailabilitySlot, pk=pk)

    if not slot.is_available:
        messages.error(request, "This slot is no longer available.")
        return redirect("book_index")

    if slot.is_in_past():
        messages.error(request, "This slot is in the past.")
        return redirect("book_index")

    intake_uuid = request.GET.get("intake")
    intake_session = None
    if intake_uuid:
        try:
            intake_session = IntakeSession.objects.filter(uuid=intake_uuid).first()
        except (ValueError, ValidationError):
            pass

    form = BookingSubmissionForm()

    return render(request, "SitePages/booking_slot.html", {
        "slot": slot,
        "form": form,
        "intake_session": intake_session,
        "intake_uuid": intake_uuid if intake_session else None,
    })

def book_submit(request, pk):
    """Handles booking form submission"""
    slot = get_object_or_404(AvailabilitySlot, pk=pk)

    # Check if slot is still available
    if not slot.is_available:
        messages.error(request, "This slot is no longer available.")
        return redirect("book_index")

    # Check if slot is in the past
    if slot.is_in_past():
        messages.error(request, "This slot is in the past.")
        return redirect("book_index")

    if request.method == "POST":
        form = BookingSubmissionForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.slot = slot

            intake_uuid = request.POST.get("intake_uuid") or request.GET.get("intake")
            if intake_uuid:
                try:
                    intake_session = IntakeSession.objects.filter(uuid=intake_uuid).first()
                    if intake_session:
                        booking.intake = intake_session
                except (ValueError, ValidationError):
                    pass

            booking.save()
            slot.is_available = False
            slot.save()
            return redirect("book_success", booking_id=booking.pk)
        else:
            intake_uuid = request.POST.get("intake_uuid") or request.GET.get("intake")
            intake_session = None
            if intake_uuid:
                try:
                    intake_session = IntakeSession.objects.filter(uuid=intake_uuid).first()
                except (ValueError, ValidationError):
                    pass
            return render(request, "SitePages/booking_slot.html", {
                "slot": slot,
                "form": form,
                "intake_session": intake_session,
                "intake_uuid": intake_uuid if intake_session else None,
            })
    else:
        return redirect("book_slot", pk=pk)

def book_success(request, booking_id):
    """Shows booking success page with QR code"""
    booking = get_object_or_404(BookingSubmission, pk=booking_id)
    qr_path = settings.BASE_DIR / "static" / "img" / "revolut-qr.png"
    return render(request, "SitePages/booking_success.html", {
        "booking": booking,
        "has_revolut_qr": qr_path.exists(),
    })

# Owner Booking Management
@login_required
@user_passes_test(is_staff_user, login_url='/')
def owner_booking_list(request):
    """Shows list of all bookings"""
    bookings = BookingSubmission.objects.all().select_related('slot')

    return render(request, "SitePages/owner_booking_list.html", {
        "bookings": bookings,
    })

@login_required
@user_passes_test(is_staff_user, login_url='/')
def owner_booking_detail(request, pk):
    """Shows detailed view of a single booking"""
    booking = get_object_or_404(BookingSubmission.objects.select_related('slot', 'intake'), pk=pk)
    return render(request, "SitePages/owner_booking_detail.html", {
        "booking": booking,
    })

@login_required
@user_passes_test(is_staff_user, login_url='/')
def owner_booking_toggle_paid(request, pk):
    """Toggle the is_paid status of a booking"""
    booking = get_object_or_404(BookingSubmission, pk=pk)

    if request.method == "POST":
        booking.is_paid = not booking.is_paid
        booking.save()
        status = "paid" if booking.is_paid else "unpaid"
        messages.success(request, f"Booking marked as {status}.")

    return redirect("owner_booking_list")

def calendar_feed(request, secret_key):
    """
    Private iCal feed for booking submissions.

    Generates a read-only ICS calendar feed containing all future bookings.
    The feed is protected by a secret key that must be included in the URL.

    Usage:
    1. Set CALENDAR_FEED_SECRET in your .env file (e.g., a random 32-character string)
    2. Subscribe to: https://yourdomain.com/calendar/<secret_key>.ics

    To subscribe in Outlook:
    - File > Account Settings > Internet Calendars > New
    - Paste the URL above
    - Outlook will refresh automatically (typically every few hours)

    To subscribe in Google Calendar:
    - Settings > Add calendar > From URL
    - Paste the URL above

    To subscribe in Apple Calendar:
    - File > New Calendar Subscription
    - Paste the URL above

    Notes:
    - This feed is READ-ONLY; changes in your calendar app won't affect the website
    - Only confirmed future bookings are included (starting from now onwards)
    - The feed updates automatically when clients book new consultations
    - Keep the URL private; anyone with the secret key can view your bookings
    - GDPR-safe: Only minimal data (name, intake ref) is included in calendar
    """
    # TEMP DIAG: confirm view is executing at all
    return HttpResponse(f"VIEW-RUNNING secret_key={secret_key!r}", status=200, content_type="text/plain")
    # Security: validate secret key
    configured_secret = settings.CALENDAR_FEED_SECRET
    if not configured_secret or secret_key != configured_secret:
        return HttpResponse("Not found", status=404)


    # Diagnostic wrapper — expose any error as plain text
    import traceback as _tb
    try:
        result = _cal_inner(request)
        return result
    except BaseException as _exc:
        _msg = f"CAL-ERROR: {type(_exc).__name__}: {_exc}\n\n{_tb.format_exc()}"
        return HttpResponse(_msg, status=200, content_type="text/plain; charset=utf-8")

def _cal_inner(request):
    from django.conf import settings
    from django.http import HttpResponse
    from django.utils import timezone
    from datetime import datetime, timezone as dt_tz
    from .models import BookingSubmission
    now = timezone.now()

    # Query all bookings (we'll filter by datetime in Python for precision)
    # Get bookings from today onwards, then filter by exact datetime
    today = now.date()
    bookings = BookingSubmission.objects.select_related('slot', 'intake').filter(
        slot__date__gte=today,
        is_paid=True,
    ).order_by('slot__date', 'slot__start_time')

    # Generate ICS content
    domain = request.get_host()

    # Helper function to escape text for ICS format
    def ics_escape(text):
        """
        Escape special characters for iCalendar text fields per RFC 5545.
        Backslash, semicolon, comma, newline must be escaped.
        """
        if not text:
            return ""
        text = str(text)
        # Order matters: escape backslash first
        text = text.replace('\\', '\\\\')
        text = text.replace(';', '\\;')
        text = text.replace(',', '\\,')
        text = text.replace('\r\n', '\\n')
        text = text.replace('\n', '\\n')
        text = text.replace('\r', '\\n')
        return text

    ics_lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        f"PRODID:-//{ics_escape(settings.SITE_NAME)}//Booking Calendar//EN",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        f"X-WR-CALNAME:{ics_escape(settings.BARRISTER_NAME)} - Consultations",
        "X-WR-TIMEZONE:UTC",
    ]

    for booking in bookings:
        slot = booking.slot

        # Combine date and time to create timezone-aware datetime objects
        start_dt = timezone.make_aware(
            datetime.combine(slot.date, slot.start_time)
        )
        end_dt = timezone.make_aware(
            datetime.combine(slot.date, slot.end_time)
        )

        # Skip if the consultation has already started (filter by start time, not end time)
        if start_dt < now:
            continue

        # Format datetimes for ICS (UTC format: YYYYMMDDTHHmmssZ)
        start_str = start_dt.astimezone(dt_tz.utc).strftime("%Y%m%dT%H%M%SZ")
        end_str = end_dt.astimezone(dt_tz.utc).strftime("%Y%m%dT%H%M%SZ")

        # Build GDPR-safe description with minimal data
        # Only include booking ID and a note to check CRM
        description_parts = []
        description_parts.append(f"Booking ID: {booking.id}")
        if booking.intake:
            description_parts.append(f"Intake Ref: {booking.intake.uuid}")
        description_parts.append("See CRM for details.")

        description = ics_escape("\n".join(description_parts))

        # Generate unique ID for this event
        uid = f"booking-{booking.id}@{domain}"

        # Use timezone.now() for DTSTAMP (not deprecated datetime.utcnow())
        dtstamp = timezone.now().astimezone(dt_tz.utc).strftime("%Y%m%dT%H%M%SZ")

        # Build client name for summary (or fallback to "Consultation")
        client_name = booking.name if booking.name else "Client"
        summary = ics_escape(f"Consultation - {client_name}")

        # Build location string with proper escaping
        location = ics_escape(f"{settings.CHAMBERS_ADDRESS_LINE1}, {settings.CHAMBERS_ADDRESS_LINE2}")

        # Create VEVENT
        ics_lines.extend([
            "BEGIN:VEVENT",
            f"UID:{uid}",
            f"DTSTAMP:{dtstamp}",
            f"DTSTART:{start_str}",
            f"DTEND:{end_str}",
            f"SUMMARY:{summary}",
            f"DESCRIPTION:{description}",
            f"LOCATION:{location}",
            "STATUS:CONFIRMED",
            "TRANSP:OPAQUE",
            "END:VEVENT",
        ])

    ics_lines.append("END:VCALENDAR")

    # Join with CRLF (required by ICS spec RFC 5545)
    ics_content = "\r\n".join(ics_lines)

    # Return as calendar file
    response = HttpResponse(ics_content, content_type="text/calendar; charset=utf-8")
    response["Content-Disposition"] = f'inline; filename="{settings.BARRISTER_NAME.replace(" ", "_")}_bookings.ics"'

    return response