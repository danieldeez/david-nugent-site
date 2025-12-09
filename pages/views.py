from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .forms import ContactForm, HomepageSettingsForm, AboutPageForm, SitePageForm, PracticeAreaForm, BlogPostForm, CaseStudyForm
import hmac, hashlib, json
import re, time, requests
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse, HttpResponseBadRequest
from .models import Booking, HomepageSettings, PracticeArea
from .models import SitePage, PracticeArea, BlogPost, CaseStudy
from django.core.cache import cache
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone

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
def book(request): return render(request, "SitePages/book.html")

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
        form = ContactForm(request.POST)
        if form.is_valid():
            lead = form.save()
            if getattr(settings, "DEFAULT_FROM_EMAIL", None) and getattr(settings, "ENQUIRY_TO_EMAIL", None):
                send_mail(
                    "New website enquiry",
                    f"Name: {lead.name}\nEmail: {lead.email}\nPhone: {lead.phone}\n\n{lead.message}",
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.ENQUIRY_TO_EMAIL],
                    fail_silently=True,
                )
            return render(request, "SitePages/thanks.html", {"lead": lead})
    else:
        form = ContactForm()
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